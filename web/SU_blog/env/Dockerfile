FROM python:3.10.12-slim-buster

RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

RUN mkdir -p /var/www/html/myblog
WORKDIR /var/www/html/myblog

COPY scripts/generate_flag.sh /tmp/generate_flag.sh
COPY scripts/readflag.c /tmp/readflag.c

RUN gcc -o /readflag /tmp/readflag.c && \
    bash /tmp/generate_flag.sh && \
    chmod 0400 /flag && \
    chown root:root /flag && \
    chmod 4755 /readflag && \ 
    rm /tmp/generate_flag.sh /tmp/readflag.c 

COPY app /var/www/html/myblog/app
COPY requirements.txt /var/www/html/myblog/

RUN pip install --no-cache-dir -r /var/www/html/myblog/requirements.txt && \
    chown -R ctf:ctf /var/www/html/myblog

USER ctf

CMD ["python", "app/app.py"]
