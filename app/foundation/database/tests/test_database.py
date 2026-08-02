from app.foundation.database import (
    Base,
    engine,
    SessionLocal,
)


def test_database_connection():

    Base.metadata.create_all(engine)

    session = SessionLocal()

    assert session is not None

    session.close()