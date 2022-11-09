import csv

import cassandra_config
from redis_cli import redis_client

from models import Document, Row, Cell


cassandra_config.init()


import hashlib
def file_as_bytes(file):
    with file:
        return file.read()


def process_csv(csv_path):
    file_md5 = hashlib.md5(
        file_as_bytes(open(csv_path, 'rb'))
    ).hexdigest()
    doc_key = f'documents:{file_md5}'
    cache_data = redis_client.hgetall(doc_key)
    print(file_md5)
    if not cache_data:
        Document(
            document_md5=file_md5,
            location=csv_path
        ).save()

    with open(csv_path) as _f:
        csv_reader = csv.DictReader(_f)

        processed_rows = int(cache_data.get('processed_rows', 0))
        current_row_counter = 0
        for row in csv_reader:
            print(f'#{current_row_counter + 1}')
            cache_data = redis_client.hgetall(doc_key)
            processed_rows = int(cache_data.get('processed_rows', 0))
            if processed_rows != 0  and current_row_counter <= processed_rows:
                current_row_counter += 1
                continue

            c_row = Row(
                document_md5=file_md5,
                document_location=csv_path,
                position=current_row_counter
            ).save()
            for field, value in row.items():
                Cell(
                    row_id=c_row.id,
                    cell_name=field,
                    cell_content=str(value)
                ).save()

            redis_client.hset(doc_key, 'processed_rows', current_row_counter)
            current_row_counter += 1

    if not redis_client.sismember('documents:process', file_md5):
        redis_client.lpush('documents:process', file_md5)

process_csv('file.csv')