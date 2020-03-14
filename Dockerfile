FROM python:3.8

RUN apt-get update -qq
RUN apt-get dist-upgrade -yqq

ADD requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt && rm -f /opt/requirements.txt

ADD bot/ /opt/bot

CMD python /opt/bot/listener.py
