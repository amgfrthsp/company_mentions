FROM python:3.9
ARG DEBIAN_FRONTEND=noninteractive
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /src
