FROM python:3.9

RUN pip3 install -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ --trusted-host mirrors.cloud.aliyuncs.com --default-timeout=60 --no-cache-dir pycryptodome

COPY ./* .

# EXPOSE 10007

CMD ["python", "m1.py"]
