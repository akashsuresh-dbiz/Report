from quart import Quart, request, send_file, jsonify
from pyppeteer import connect
import asyncio
import logging

app = Quart(__name__)

logging.basicConfig(level=logging.INFO)


async def render_pdf(url, output_path):
    browser = None
    page = None
    try:
        logging.info(f"Connecting to browser")
        browser = await connect(browserWSEndpoint="ws://browserless:3000/")
        logging.info(f"Connected to browser. Opening new page for URL: {url}")
        page = await browser.newPage()
        await page.setViewport({'width': 1080, 'height': 1080})
        await page.goto(url, {'waitUntil': 'networkidle2'})
        await page.waitForSelector('body')
        await asyncio.sleep(10)
        logging.info(f"Rendering PDF for URL: {url}")
        await page.screenshot({
            'path': 'fullpage.png',
            'fullPage': True

        })
        await page.pdf({
        'path': output_path,
        # 'format': 'A4',  # or 'Letter' for a US Letter format
        'printBackground': True,
        'width': '1920px',
        # 'scale': 0.95,
        'height': '1080px',
        # 'preferCSSPageSize': True,
        'landscape': True
        })
    except Exception as e:
        logging.error(f"Error in render_pdf: {e}")
    finally:
        if page:
            await page.close()
        if browser:
            await browser.close()
        logging.info(f"Browser closed")

@app.route('/generate_pdf', methods=['GET'])
async def generate_pdf():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    output_path = 'output.pdf'

    try:
        await render_pdf(url, output_path)
    except Exception as e:
        logging.error(f"Error in generate_pdf: {e}")
        return jsonify({'error': str(e)}), 500

    return await send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
