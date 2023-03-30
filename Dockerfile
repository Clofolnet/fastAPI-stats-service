# syntax=docker/dockerfile:1
FROM python:3.8.10

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_SERVER=${POSTGRES_SERVER}
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV POSTGRES_DB=${POSTGRES_DB}

EXPOSE 80

WORKDIR ./app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]