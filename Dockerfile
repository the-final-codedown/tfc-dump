FROM python:3.8.1-alpine3.11

RUN pip install --no-cache-dir falcon gunicorn requests

ADD dump.py ./

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8085 'dump:setup_dump(\"http://account:8081\",\"http://profile:8083\")'"]


