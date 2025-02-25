FROM python:latest

# Set the working directory
WORKDIR /app
COPY  main.py /app
COPY  audit.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "/app/main.py"]

EXPOSE 5000