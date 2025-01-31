FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /var/www/html/project/api

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
libjpeg-dev \
zlib1g-dev \
libhdf5-dev \
gcc \
pkg-config \
python3-dev \
&& rm -rf /var/lib/apt/lists/* 



RUN pip3 install --upgrade pip && pip3 install --timeout=60 --retries=5 -r requirements.txt

COPY . /var/www/html/project/api

# COPY tb_api.sh /var/www/html/project/api/tb_api.sh
# RUN chmod +x /var/www/html/project/api/tb_api.sh
