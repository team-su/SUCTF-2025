FROM php:7.3-cli

COPY files /tmp/files/


COPY src /tmp/suctf_web/


RUN chown -R www-data:www-data /tmp/suctf_web && \
    chmod -R 755 /tmp/suctf_web && \
    mv /tmp/files/flag.sh / && \
    mv /tmp/files/start.sh / && \
    mv /tmp/files/seef1ag_getfl4g / && \
    chmod +x /flag.sh /start.sh && \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i '/security/d' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y libzip-dev build-essential libaio1 libnuma1 psmisc libmecab2 && \
    docker-php-ext-configure zip && \
    docker-php-ext-install zip && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/files
    

ENV FLAG=SUCTF{}
CMD ["/start.sh"]


EXPOSE 80
