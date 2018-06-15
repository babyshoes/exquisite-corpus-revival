FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y vim
RUN apt-get install -y python-pip python-dev build-essential
COPY . /home/app
WORKDIR /home/app
RUN pip install -r requirements.txt
ENV POSTGRES_USER exquisite
ENV POSTGRES_PASSWORD corpse
ENV POSTGRES_DB exq_db
ENV FLASK_APP app.py
# RUN python -c 'from database import *; init_db()'
# RUN flask db init
# RUN flask db migrate

# CMD flask run --host=0.0.0.0
# CMD python -c 'from database import *; init_db()' && flask run --host=0.0.0.0

CMD python -m flask run --host=0.0.0.0