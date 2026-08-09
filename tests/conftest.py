import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app

from app.foundation.database import Base

from app.domains.assets.documents.models import (
    DocumentModel,
)

from app.domains.assets.documents.bootstrap import (
    document_repository,
)


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def documents_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "documents_test.db"
    )

    test_engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        echo=False,
        future=True,
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(
        test_engine
    )

    monkeypatch.setattr(
        document_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield document_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()