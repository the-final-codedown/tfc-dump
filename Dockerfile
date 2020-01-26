FROM alexisgra/falcon-alpine-python-3.7.4:latest

ADD dump.py ./

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8084 'dump:setup_dump(\"http://account:8081\",\"http://profile:8083\")'"]


