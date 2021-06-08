FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

COPY apt_requirements.txt /code/
RUN apt-get update && cat apt_requirements.txt | xargs apt -y install

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /code/
RUN pip install -r requirements.txt

ENTRYPOINT /code/entrypoint.sh