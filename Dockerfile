FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

RUN pip3 install wheel
RUN pip3 install gunicorn

COPY ./ /aplocation
WORKDIR /aplocation

RUN pip3 install .

CMD python3 wsgi.py