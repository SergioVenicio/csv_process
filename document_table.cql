CREATE KEYSPACE IF NOT EXISTS documents WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

CREATE TABLE IF NOT EXISTS documents.documents (
    document_md5 TEXT,
    location TEXT,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (document_md5)
);

CREATE TABLE IF NOT EXISTS documents.rows (
    id UUID,
    document_md5 TEXT,
    position int,
    PRIMARY KEY(id, document_md5)
);

CREATE TABLE IF NOT EXISTS documents.cells (
    id UUID,
    row_id UUID,
    cell_name TEXT,
    cell_content TEXT,
    PRIMARY KEY(id, row_id)
);