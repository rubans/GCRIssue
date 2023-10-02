FROM python:3.9.5-buster

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
COPY modules /app
#COPY proxy-certs /app
EXPOSE 8080
ENV PORT 8080

WORKDIR /app

CMD exec gunicorn --bind :$PORT sync_bot:app --workers 1 --threads 1 --timeout 60

