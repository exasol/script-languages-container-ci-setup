FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install \
        openjdk-17-jdk \
        locales \
        python3.10-venv \
        python3-pip \
        unixodbc \
        unixodbc-dev \
        curl \
        git && \
    locale-gen en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 && \
    apt-get -y clean && \
    apt-get -y autoremove && \
    ldconfig

RUN curl -fsSL https://get.docker.com | bash

RUN mkdir -p downloads/ODBC downloads/JDBC downloads/EXAplus
RUN curl -s https://x-up.s3.amazonaws.com/7.x/24.1.1/Exasol_ODBC-24.1.1-Linux_x86_64.tar.gz  | tar -C downloads/ODBC --strip-components 2 -zxf -
RUN curl -s https://x-up.s3.amazonaws.com/7.x/24.1.1/Exasol_JDBC-24.1.1.tar.gz | tar -C downloads/JDBC --strip-components 2 -zxf -
RUN curl -s https://x-up.s3.amazonaws.com/7.x/24.1.1/EXAplus-24.1.1.tar.gz | tar -C downloads/EXAplus --strip-components 2 -zxf -
ENV EXAPLUS=/downloads/EXAplus/exaplus

COPY deps/requirements.txt requirements.txt
RUN pip3 install -r "requirements.txt"
