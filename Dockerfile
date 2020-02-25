FROM python:3.8.1-alpine3.11

RUN pip install --no-cache-dir falcon gunicorn requests
ENV ACCOUNT=http://tfc-account:8081
ENV PROFILE=http://tfc-profile:8083
ADD dump.py ./

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8085 'dump:setup_dump(\"http://tfc-account:8081\",\"http://tfc-profile:8083\")'"]


