FROM python:3.10
WORKDIR /kafka_to_clickhouse/tests
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT pytest ./src