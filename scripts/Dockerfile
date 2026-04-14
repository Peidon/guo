FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY scripts/requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && python -m playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/generate_overnight_report.py /app/generate_overnight_report.py

VOLUME ["/work"]

ENTRYPOINT ["python", "/app/generate_overnight_report.py"]
CMD ["--output", "/work/overnight_data_generated.xlsx", "--prefer-browser"]
