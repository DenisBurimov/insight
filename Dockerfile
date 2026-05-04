# Stage 1: build — compile Python wheels without system bloat
FROM python:3.13-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --target=/install -r requirements.txt && \
    pip install --no-cache-dir --target=/install gunicorn ipython


# Stage 2: runtime — add system deps and copy compiled packages
FROM python:3.13-slim

# Firefox + geckodriver are required at runtime for OCR (Selenium)
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep "tag_name" | cut -d '"' -f 4) \
    && wget -qO- "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" \
    | tar -xz -C /usr/local/bin

COPY --from=builder /install /usr/local/lib/python3.13/site-packages/

RUN useradd --uid 2001 --create-home app
USER app
WORKDIR /home/app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    FLASK_APP=wsgi.py \
    PORT=8080

COPY --chown=app:app . .

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
