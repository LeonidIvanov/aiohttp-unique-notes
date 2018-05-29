from sqlalchemy import create_engine, MetaData

from unique_notes.settings import config
from unique_notes.db import note


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[note])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(note.insert(), [
        {'title': 'Sample note',
         'meta_description': 'First sample note meta desctiption',
         'description': "Deadlights interloper execution dock wherry pink jolly boat barkadeer clipper yo-ho-ho hands dance the hempen jig case shot broadside Sail ho Cat o'nine tails draft carouser schooner boom gally. Spyglass lugsail loaded to the gunwalls Jack Tar pink carouser pinnace scuttle grog blossom plunder black jack bilge rat rutters belaying pin jack heave down pressgang execution dock piracy flogging.",
         'unique_words': 52}
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
