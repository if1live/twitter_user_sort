FROM ubuntu:14.04
MAINTAINER if1live <libsora25@gmail.com>

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN \
  apt-get update &&\
  apt-get -qq -y install git wget unzip

RUN \
  apt-get -qq -y install python-virtualenv python-pip python2.7-dev

# Install foreman
RUN \
  wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh

RUN \
  mkdir -p /var/www

RUN \
  cd /tmp/ &&\
  wget https://github.com/if1live/twitter_user_sort/archive/master.zip &&\
  unzip master.zip &&\
  mv twitter_user_sort-master /var/www/twitter_user_sort

WORKDIR /var/www/twitter_user_sort

RUN \
  virtualenv .venv &&\
  source .venv/bin/activate &&\
  pip install -r requirements.txt

EXPOSE 5000
CMD \
  source .venv/bin/activate &&\
  echo "TWITTER_API_KEY=$TWITTER_API_KEY" &&\
  echo "TWITTER_SECRET_KEY=$TWITTER_SECRET_KEY" &&\
  foreman start -f Procfile




