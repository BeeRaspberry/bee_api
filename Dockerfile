FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install -y postgresql sqlite3

COPY ./requirements.txt /app/requirements.txt
COPY migrations /app/migrations
COPY ./app /app/app
COPY ./seed /app/seed
COPY ./config-sample /app/config.py
COPY ./helpers /app/helpers
COPY ./main.py /app/main.py
COPY prestart.sh /app/prestart

RUN pip install -r requirements.txt

# The SED commands replace the Windows characters
RUN sed -e "s/\r//g" /app/prestart > /app/prestart.sh

WORKDIR /app

EXPOSE 80

ENV FLASK_APP=main.py
