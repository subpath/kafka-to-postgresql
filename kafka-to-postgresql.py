"""Kafka to PSQL script."""
# built-in
import json
import sys
import uuid

# external
from pykafka import KafkaClient
from pykafka.common import OffsetType
import toml
import pandas as pd

# project
from create_engine import engine

CONFIG = toml.load('config.toml')


def parse_uid(message:dict, uid_columns:list=['user_id_got', 'user_id_set']):
    """Parce uuid fields"""
    for column in uid_columns:
        if 'uid' in message[column]:
            message[column] = str(uuid.UUID(message[column].replace('uid=','')))
    return message

# start Kafka consumer
client = KafkaClient(hosts=CONFIG['kafka_connector']['broker'])

consumer = client.topics[CONFIG['kafka_connector']['topic']].get_balanced_consumer(
    consumer_group=CONFIG['kafka_connector']['consumer_group'],
    auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=True)


print('Starting consumer')
for message in consumer:
    try:
        value = json.loads(message.value)
        value = parse_uid(value)
        df = pd.DataFrame(value, index=[0])
        df = df.replace({'-': None})
        df.to_sql(CONFIG['psql_connector']['table'],
                con=engine,
                if_exists="append", index=False)

    except Exception as e:
        print(e)



