FROM sagemath/sagemath:10.5
LABEL auther_template="CTF-Archives"

USER root

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@//.*security.ubuntu.com@//mirrors.aliyun.com@g' /etc/apt/sources.list
RUN apt-get update 

RUN apt-get install -y socat 
USER sage
RUN sage --python -m pip install -i https://mirrors.aliyun.com/pypi/simple \
    pycryptodome


COPY ./src/main.sage /home/sage
COPY ./service/docker-entrypoint.sh /home/sage/docker-entrypoint.sh


ENTRYPOINT ["/bin/bash","/home/sage/docker-entrypoint.sh"]