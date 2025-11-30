FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends cron tzdata && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app.py crypto_utils.py ./
COPY scripts/log_2fa_cron.py scripts/
COPY cron/2fa-cron cron/
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron
RUN mkdir -p /data /cron && chmod 755 /data /cron
EXPOSE 8080
CMD ["sh", "-c", "cron && python app.py"]
