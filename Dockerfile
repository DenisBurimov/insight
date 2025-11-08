FROM python:3.13

# Установим Firefox и зависимости
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN firefox --version || (echo "❌ Firefox not installed or broken!" && exit 1)
RUN if ! firefox --version >/dev/null 2>&1; then \
      echo "❌ Firefox is not installed or not working!" && exit 1; \
    fi


# Установим geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep "tag_name" | cut -d '"' -f 4) \
    && wget -qO- https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    | tar -xz -C /usr/local/bin

# Add user app
RUN python -m pip install -U pip
RUN adduser -uid 2001 app
USER app
WORKDIR /home/app

# Set environment variables
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PATH="/home/app/.local/bin:${PATH}"

# Install app dependencies
COPY --chown=app:app requirements.txt /home/app/requirements.txt

RUN pip install --user --no-cache-dir -r requirements.txt
RUN pip install --user gunicorn ipython

COPY --chown=app:app . .
ENV PORT 8080
ENV FLASK_APP=wsgi.py


EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
