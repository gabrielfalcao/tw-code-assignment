FROM ubuntu:14.04

ENV DEBIAN_FRONTEND  noninteractive
ENV PYTHONUNBUFFERED true
ENV VIRTUAL_ENV      /srv/venv
ENV PATH             $VIRTUAL_ENV/bin:$PATH

MAINTAINER gabriel@nacaolivre.org

RUN apt-get update \
  && apt-get --yes install \
    build-essential \
    ca-certificates \
    coreutils \
    python-pip \
    python2.7 \
    python2.7-dev \
    vim \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip virtualenv
RUN mkdir -p /srv/{src,venv}
RUN virtualenv /srv/venv

#COPY . /srv/src/

WORKDIR /srv/src
RUN pip install -r development.txt
CMD ["","--help"]
