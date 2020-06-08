FROM python:3

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py

ADD . /code/
CMD flask run --host=0.0.0.0
