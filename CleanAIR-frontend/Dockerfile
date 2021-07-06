FROM ubuntu:20.04

WORKDIR /usr/src/clean_air_frontend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV prod

# Install the webserver and Python
RUN apt-get update
    # && apt-get -y install nginx

RUN apt-get -y install  python3 \
                        python3-dev \
                        python3-pip

# Install the application container
# RUN pip3 install uwsgi

# Install the application requirements
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# RUN apk add python-psycopg2
# RUN pip3 install psycopg2-binary
RUN apt-get install -y libpq-dev && \
    apt-get install -y python3-psycopg2  && \
    pip3 install psycopg2

# Copy all project files
COPY . .

# configure the webserver
# COPY clean_air_frontend_nginx.conf /etc/nginx/sites-available/mysite_nginx.conf
# RUN ln -s /etc/nginx/sites-available/mysite_nginx.conf /etc/nginx/sites-enabled/

# Start the webserver
EXPOSE 80
# CMD nginx -g "daemon off;"; uwsgi --ini uwsgi.ini;
CMD python3 manage.py runserver 0.0.0.0:80