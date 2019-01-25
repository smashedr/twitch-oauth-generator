FROM python:3.6-alpine
ENV TZ=America/Los_Angeles

RUN apk add --update --no-cache \
    alpine-sdk \
    bash \
    build-base \
    freetype-dev \
    jpeg-dev \
    lcms2-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    mysql-dev \
    openjpeg-dev \
    openldap-dev \
    pcre \
    pcre-dev \
    python3 \
    python3-dev \
    py3-pip \
    tiff-dev \
    tk-dev \
    tcl-dev \
    zlib-dev

WORKDIR /app
COPY requirements.txt /app

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
