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

from app.domains.assets.photos.models import (
    PhotoModel,
)

from app.domains.assets.photos.bootstrap import (
    photo_repository,
)

from app.domains.assets.maintenance_history.models import (
    MaintenanceEventModel,
)

from app.domains.assets.maintenance_history.bootstrap import (
    maintenance_event_repository,
)


from app.domains.identity.people.models import (
    PersonModel,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)


from app.domains.identity.roles.models import (
    RoleModel,
)

from app.domains.identity.roles.bootstrap import (
    role_repository,
)


from app.domains.identity.users.models import (
    UserModel,
)

from app.domains.identity.users.bootstrap import (
    user_repository,
)

from app.domains.assets.preventive_maintenance.bootstrap import (
    preventive_maintenance_execution_repository,
    preventive_maintenance_repository,
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
def authenticated_client(
    client,
):

    with client.session_transaction() as session:

        session["username"] = "test-admin"
        session["person_code"] = "TEST-001"
        session["role_code"] = "ADMIN"

    return client

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

@pytest.fixture
def photos_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "photos_test.db"
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
        photo_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield photo_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()

@pytest.fixture
def maintenance_history_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "maintenance_history_test.db"
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
        maintenance_event_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield maintenance_event_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()

@pytest.fixture
def preventive_maintenance_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "preventive_maintenance_test.db"
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

    yield preventive_maintenance_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()


@pytest.fixture
def people_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "people_test.db"
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
        person_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield person_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()



@pytest.fixture
def roles_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "roles_test.db"
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
        role_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield role_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()


@pytest.fixture
def users_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "users_test.db"
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
        user_repository,
        "_session_factory",
        TestSessionLocal,
    )

    yield user_repository

    Base.metadata.drop_all(
        test_engine
    )

    test_engine.dispose()

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

@pytest.fixture
def preventive_execution_web_test_db(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path
        / "preventive_execution_web_test.db"
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