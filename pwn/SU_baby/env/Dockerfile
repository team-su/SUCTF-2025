FROM ubuntu:18.04

RUN sed -i 's/archive.ubuntu.com/asia-east1.gce.archive.ubuntu.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
#apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*

COPY ./pwn.xinetd /etc/xinetd.d/pwn

COPY ./service.sh /service.sh

RUN chmod +x /service.sh

# useradd and put flag
RUN useradd -m 01 && useradd -m ASU1 && echo 'SUCTF{084e4d64-cba3-4141-9b99-7412cdd6a33d}' > /home/01/flag.txt && echo 'SUCTF{084e4d64-cba3-4141-9b99-7412cdd6a33d}' > /home/ASU1/flag.txt

# copy bin
COPY ./bin/01 /home/01/01
COPY ./catflag /home/01/bin/sh
COPY ./bin/ASU1 /home/ASU1/ASU1
COPY ./catflag /home/ASU1/bin/sh


# chown & chmod
RUN chown -R root:01 /home/01 && chmod -R 750 /home/01 && chmod 740 /home/01/flag.txt && chown -R root:ASU1 /home/ASU1 && chmod -R 750 /home/ASU1 && chmod 740 /home/ASU1/flag.txt

# copy lib,/bin 
RUN cp -R /lib* /home/01 && cp -R /usr/lib* /home/01 && mkdir /home/01/dev && mknod /home/01/dev/null c 1 3 && mknod /home/01/dev/zero c 1 5 && mknod /home/01/dev/random c 1 8 && mknod /home/01/dev/urandom c 1 9 && chmod 666 /home/01/dev/* && cp /bin/sh /home/01/bin && cp /bin/ls /home/01/bin && cp /bin/cat /home/01/bin && cp -R /lib* /home/ASU1 && cp -R /usr/lib* /home/ASU1 && mkdir /home/ASU1/dev && mknod /home/ASU1/dev/null c 1 3 && mknod /home/ASU1/dev/zero c 1 5 && mknod /home/ASU1/dev/random c 1 8 && mknod /home/ASU1/dev/urandom c 1 9 && chmod 666 /home/ASU1/dev/* && cp /bin/sh /home/ASU1/bin && cp /bin/ls /home/ASU1/bin && cp /bin/cat /home/ASU1/bin

CMD ["/service.sh"]
