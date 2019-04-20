FROM python:3.6.8-alpine3.9

RUN apk update && apk add \
    git nano php

ADD . /git-php-lint-base

WORKDIR /git-php-lint-base

RUN python setup.py install

RUN git clone https://github.com/thedevdojo/php-login-script.git /login

RUN echo 'echo "hello world" ' >> /login/logout.php

WORKDIR /login