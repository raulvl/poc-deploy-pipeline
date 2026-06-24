FROM python:3.11-slim

WORKDIR /app
COPY app.py .

ARG BUILD_SHA=unknown
ENV APP_VERSION=$BUILD_SHA

EXPOSE 8080
CMD ["python", "app.py"]
