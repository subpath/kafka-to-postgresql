FROM python:3.7
WORKDIR /project
ADD . /project
RUN  apt-get update\
    && apt-get install libsnappy-dev -y \
    && pip install -r requirements.txt

CMD ["python", "kafka-to-postgresql.py"]