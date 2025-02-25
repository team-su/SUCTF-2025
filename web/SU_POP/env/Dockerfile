FROM php:8.4-apache

# Apache 初始化
RUN a2enmod rewrite

# 配置mysql
RUN docker-php-source extract && \
    docker-php-ext-install pdo_mysql mysqli && \
    docker-php-source delete

# 安装必要的软件包
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    # apk add --update --no-cache tar apache mysql mysql-client bash
    apt update && \
    apt install -y unzip

RUN apt-get update && \
    apt-get install -y libicu-dev && \
    docker-php-ext-install intl && \
    apt-get clean
# 重新设置源码路径的用户所有权
RUN chown -R www-data:www-data /var/www/html

# 拷贝容器入口点脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod 777 /docker-entrypoint.sh

# 设置shell的工作目录
WORKDIR /var/www/html

COPY ./src/cakephp-5-1-4.zip /var/www/html/

RUN unzip cakephp-5-1-4.zip

COPY ./src/routes.php config/routes.php
COPY ./src/PagesController.php src/Controller/PagesController.php
COPY ./src/handle_ser.php src/View/handle_ser.php
COPY ./src/app_local.php config/app_local.php
COPY ./src/flag.txt /flag.txt

RUN chmod +x bin/cake
RUN chmod +s /usr/bin/find
RUN chmod 400 /flag.txt
EXPOSE 80
USER www-data
# 设置容器入口点
ENTRYPOINT [ "/docker-entrypoint.sh" ]
