FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

RUN pip3 install wheel
RUN pip3 install gunicorn

COPY ./ /aplocation
WORKDIR /aplocation

RUN pip3 install .

EXPOSE 5000

CMD python3 wsgi.py
# This potentially breaks because of an ENV issue with gunicorn. Add logging to test.
# CMD gunicorn --bind 0.0.0.0:5000 wsgi:app