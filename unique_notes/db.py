import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, Text,
    Integer, String
)

from .utils import unique_word_count

__all__ = ['note']

meta = MetaData()

note = Table(
    'note', meta,

    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(200), nullable=False),
    Column('meta_description', String(300), nullable=False),
    Column('description', Text, nullable=False),
    Column('unique_words', Integer, nullable=False),
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_note(conn, note_id):
    result = await conn.execute(
        note.select()
        .where(note.c.id == note_id))
    note_record = await result.first()
    if not note_record:
        msg = "note with id: {} does not exists"
        raise RecordNotFound(msg.format(note_id))
    return note_record


async def note_create(conn, title, description):
    result = await conn.execute(note.insert().values(
        title=title,
        meta_description='{}...'.format(description[:295]),
        description=description,
        unique_words=unique_word_count(description))
    )
    note_record = await result.fetchone()
    return note_record[0]
