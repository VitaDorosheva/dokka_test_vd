from sqlalchemy.orm.session import Session
from sqlalchemy.sql.dml import Insert
from typing import Iterable


def chunks(values, max_chunk_size):
    chunk = []

    for value in values:
        if len(chunk) == max_chunk_size:
            yield chunk
            chunk = []
        chunk.append(value)
    yield chunk


def bulk_insert(session: Session, table, values: Iterable[dict], chunk_size: int = 1000):
    for values_chunk in chunks(values, chunk_size):
        if not values_chunk:
            break
        stmt = Insert(table, values_chunk)
        session.execute(stmt)