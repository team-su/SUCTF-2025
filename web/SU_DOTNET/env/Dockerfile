FROM mono:6.12.0.182


RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt update && apt install -y nginx supervisor xvfb \
&& rm -rf /var/lib/apt/lists/*

COPY ./app /app
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./readflag /readflag
COPY ./flag.txt /flag.txt

RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag


RUN useradd --create-home --shell /bin/bash ctf

RUN chown -R ctf:ctf /app

RUN rm -rf /tmp/*

WORKDIR /app

EXPOSE 80

RUN nginx -t

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
