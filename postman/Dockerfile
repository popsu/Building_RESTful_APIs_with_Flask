FROM ubuntu:19.04

RUN apt-get update \
    && apt-get install -y \
    libgtk-3-0 \
    libnss3-dev \
    libx11-xcb-dev \
    libxss1 \
    libasound2-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.pstmn.io/download/latest/linux64 -O postman-linux-x64.tar.gz \
    && tar -xvzf postman-linux-x64.tar.gz -C /opt \
    && ln -s /opt/Postman/Postman /usr/bin/postman \
    && rm postman-linux-x64.tar.gz

RUN apt-get update && apt-get install -y aptitude

ENTRYPOINT [ "postman" ]
