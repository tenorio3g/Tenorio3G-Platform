import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.preventive_maintenance.bootstrap import (
    preventive_maintenance_execution_repository,
    preventive_maintenance_repository,
)


@pytest.fixture
def preventive_maintenance_execution_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "preventive_maintenance_execution_test.db"
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
        preventive_maintenance_repository,
        "_session_factory",
        TestSessionLocal,
    )

    monkeypatch.setattr(
        preventive_maintenance_execution_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield (
        preventive_maintenance_repository,
        preventive_maintenance_execution_repository,
    )

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()