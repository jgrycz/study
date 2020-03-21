FROM resin/raspberry-pi-python

LABEL "maintainer"="jaroslaw.grycz@gmail.com"

USER root

ENV APP /data/app
ENV APP_FILE leds_and_buttons.py

# Application Code
ADD $APP_FILE $APP/

WORKDIR $APP

RUN pip install RPi.GPIO

CMD python $APP_FILE

