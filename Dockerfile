FROM python:3.7-slim AS python-slim

# uwsgi, adapted from https://github.com/docker-library/python.git
# in file python/3.7/slim/Dockerfile
RUN set -ex \
    && buildDeps=' \
        gcc \
        libbz2-dev \
        libc6-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libpcre3-dev \
        make \
        tcl-dev \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev \
    ' \
    && deps=' \
        libexpat1 \
    ' \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends  && rm -rf /var/lib/apt/lists/* \
    && pip install uwsgi \
    && apt-get purge -y --auto-remove $buildDeps \
    && find /usr/local -depth \
    \( \
        \( -type d -a -name test -o -name tests \) \
        -o \
        \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    \) -exec rm -rf '{}' +

CMD ["python3"]

FROM python-slim AS container-image

RUN apt-get update && apt-get install -y \
    uwsgi \
    nginx \
    supervisor

COPY ./config_files/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./config_files/confd_nginx.conf /etc/nginx/nginx.conf

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./config_files/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./config_files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app

RUN mkdir -p /spool/nginx /run/pid && \
    adduser --system nginx && \
    addgroup --system nginx && \
    chmod -R 777 /var/log/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
#    chown -R nginx:nginx /app && \
    chgrp -R 0 /var/log/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX /var/log/nginx /etc/nginx /var/run /run /run/pid /spool/nginx
#    touch /var/log/supervisor/supervisord.log && \


#USER nginx:nginx

CMD ["/usr/bin/supervisord"]


FROM container-image

COPY ./requirements.txt /app/requirements.txt

#WORKDIR /app

RUN pip install -r requirements.txt

COPY ./uwsgi.py /app/uwsgi.py

COPY migrations /app/migrations
COPY ./app /app/app
COPY ./seed /app/seed
COPY ./config-sample.py /app/config.py
COPY ./helpers /app/helpers
COPY ./main.py /app/main.py
COPY ./entrypoint.sh /app/entrypoint

# The SED commands replace the Windows characters
RUN sed -e "s/\r//g" /app/entrypoint > /app/entrypoint.sh && chmod u+x /app/entrypoint.sh

ENV FLASK_APP=main.py
ENV PATH="/home/nginx/.local/bin:${PATH}"

CMD ["/app/entrypoint.sh"]
#CMD ["sleep", "600"]