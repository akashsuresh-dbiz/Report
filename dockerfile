FROM python:3.9-slim
LABEL maintainer="dbiz.ai"

ENV PYTHONUNBUFFERED 1


COPY requirements.txt /temp/requirements.txt
COPY ./ /app

WORKDIR /app
EXPOSE 3000

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /temp/requirements.txt && \
    apt-get update && \
    rm -rf /temp && \
    adduser \
        --disabled-password \
        --no-create-home \
        cloud-app-user

ENV PATH="/py/bin:$PATH"

USER root
CMD ["python", "app.py"]
