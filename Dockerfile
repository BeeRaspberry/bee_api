FROM python:3.7.3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r ./requirements.txt

COPY . .

COPY migrations /app/migrations
COPY ./app /app/app
COPY ./seed /app/seed
# attempt to fix layering issue when running on Github action
RUN true
COPY ./config-sample.py /app/config.py
COPY ./helpers /app/helpers
COPY ./main.py /app/main.py
COPY ./entrypoint.sh /app/entrypoint

# The SED commands replace the Windows characters
RUN sed -e "s/\r//g" /app/entrypoint > /app/entrypoint.sh && chmod u+x /app/entrypoint.sh

ENV FLASK_APP=main.py
ENV PATH="/home/nginx/.local/bin:${PATH}"

CMD ["/app/entrypoint.sh"]
