from datetime import datetime
import uuid

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

class Document(Model):
    __keyspace__ = 'documents'
    __table_name__ = 'documents'

    document_md5 = columns.Text(primary_key=True)
    location = columns.Text()
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime()


class Row(Model):
    __keyspace__ = 'documents'
    __table_name__ = 'rows'

    id = columns.UUID(default=uuid.uuid4, primary_key=True)
    document_md5 = columns.Text(primary_key=True)
    position = columns.Integer()


class Cell(Model):
    __keyspace__ = 'documents'
    __table_name__ = 'cells'

    id = columns.UUID(default=uuid.uuid4, primary_key=True)
    row_id = columns.UUID(primary_key=True)
    cell_name = columns.Text()
    cell_content = columns.Text()