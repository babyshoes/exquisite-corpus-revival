FROM python:3.6.5-alpine

COPY . /home/app
WORKDIR /home/app

RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

ENV POSTGRES_USER exquisite
ENV POSTGRES_PASSWORD corpse
ENV POSTGRES_DB exq_db
ENV FLASK_APP app.py

CMD python -m flask run --host=0.0.0.0