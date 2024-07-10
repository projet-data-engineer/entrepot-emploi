FROM apache/airflow:2.9.0

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         wget \
         unzip \
         git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt