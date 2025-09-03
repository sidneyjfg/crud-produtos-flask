from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
Session = None

def init_engine_and_session(database_url: str):
    global engine, Session
    engine = create_engine(database_url, pool_pre_ping=True, future=True)
    Session = scoped_session(
        sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    )
    return engine, Session
