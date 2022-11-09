
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from models import Document, Row, Cell


def init():
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster([
        '127.0.0.1'
    ], auth_provider=auth_provider)

    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    sync_table(Document)
    sync_table(Row)
    sync_table(Cell)