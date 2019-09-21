FROM ubuntu:18.04
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN apt-get install git -y
RUN apt-get install python2.7-dev python-pip python-requests python-virtualenv python-rpy2 postgresql postgresql-contrib libpq-dev python-psycopg2 containerd -y
RUN apt-get install systemd -y


RUN mkdir galaxyDir
WORKDIR galaxyDir
RUN git clone --branch v1.0.0 https://github.com/madgik/galaxy
COPY galaxy.yml galaxy/config/galaxy.yml
COPY galaxy.yml galaxy/config/galaxy.yml
COPY exareme_env.py /srv/executor/tools/exaremeTools/exareme_environment.py
RUN cat galaxy/config/galaxy.yml
WORKDIR galaxy

RUN apt-get install apache2 -y
RUN apt-get install apache2 libapache2-mod-proxy-uwsgi -y
RUN a2enmod headers deflate expires rewrite proxy proxy_uwsgi
RUN a2enmod proxy_http

WORKDIR /etc/apache2/sites-available/
COPY galaxy.conf ./galaxy.conf
RUN cat galaxy.conf
RUN chown root:root galaxy.conf
WORKDIR /etc/apache2/sites-enabled/
RUN ln -s ../sites-available/galaxy.conf galaxy.conf
RUN rm -rf 000-default.conf
RUN htpasswd -bc /etc/apache2/htpasswd  username password

WORKDIR /galaxyDir/galaxy
