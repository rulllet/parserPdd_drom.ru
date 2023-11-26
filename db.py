from contextlib import contextmanager
from sqlmodel  import create_engine, Session


sqlite_file_name = "sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)


@contextmanager
def session_scope():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()