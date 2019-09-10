FROM python:3.7.4
WORKDIR /app
COPY ./ ./
RUN pip install open-nsfw-python3
RUN apt update && apt install caffe-cpu --yes
ENV PYTHONPATH=/usr/lib/python3/dist-packages:
