from io import BytesIO
from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)
from app.domains.identity.users.bootstrap import (
    password_hasher,
)


def test_assets_index_should_require_login(
    client,
) -> None:

    response = client.get(
        "/activos",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )

def test_assets_index_should_respond_when_authenticated(
    client,
) -> None:

    with client.session_transaction() as session:

        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200


def test_create_document_form_should_respond(
    authenticated_client,
) -> None:

    response = authenticated_client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 200

    assert b"Registrar documento" in response.data


def test_create_document_should_persist_and_redirect(
    authenticated_client,
    documents_test_db,
) -> None:

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-DOC-HTTP-001",
            "title": "Manual de prueba",
            "document_type": "manual",
            "file_name": "manual_test.pdf",
            "revision": "A",
            "description": (
                "Documento creado desde "
                "una prueba HTTP."
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = documents_test_db.get_by_code(
        "TEST-DOC-HTTP-001"
    )

    assert persisted is not None
    assert persisted.asset_code == "S2-480-ES09-T269"
    assert persisted.title == "Manual de prueba"
    assert persisted.document_type == "manual"
    assert persisted.file_name == "manual_test.pdf"
    assert persisted.revision == "A"


def test_edit_document_should_update_and_redirect(
    authenticated_client,
    documents_test_db,
) -> None:

    # Primero creamos el documento de prueba.
    authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-DOC-HTTP-EDIT",
            "title": "Manual original",
            "document_type": "manual",
            "file_name": "manual_original.pdf",
            "revision": "A",
            "description": "Versión original.",
        },
        follow_redirects=False,
    )

    # Ahora lo editamos mediante HTTP.
    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/"
            "TEST-DOC-HTTP-EDIT/"
            "editar"
        ),
        data={
            "title": "Manual actualizado",
            "document_type": "manual",
            "file_name": "manual_actualizado.pdf",
            "revision": "B",
            "description": "Versión actualizada.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = documents_test_db.get_by_code(
        "TEST-DOC-HTTP-EDIT"
    )

    assert persisted is not None
    assert persisted.title == "Manual actualizado"
    assert persisted.file_name == "manual_actualizado.pdf"
    assert persisted.revision == "B"
    assert persisted.description == "Versión actualizada."

def test_delete_document_should_remove_and_redirect(
    authenticated_client,
    documents_test_db,
) -> None:

    # Creamos primero el documento de prueba.
    authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-DOC-HTTP-DELETE",
            "title": "Documento para eliminar",
            "document_type": "manual",
            "file_name": "delete_test.pdf",
            "revision": "A",
            "description": "Documento temporal.",
        },
        follow_redirects=False,
    )

    persisted = documents_test_db.get_by_code(
        "TEST-DOC-HTTP-DELETE"
    )

    assert persisted is not None

    # Lo eliminamos mediante la ruta HTTP.
    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/"
            "TEST-DOC-HTTP-DELETE/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    deleted = documents_test_db.get_by_code(
        "TEST-DOC-HTTP-DELETE"
    )

    assert deleted is None

def test_upload_pdf_should_persist_document(
    authenticated_client,
    documents_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.documents.storage import (
        LocalDocumentStorage,
    )

    test_storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    monkeypatch.setattr(
        routes,
        "document_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-PDF-001",
            "title": "Manual PDF de prueba",
            "document_type": "manual",
            "revision": "A",
            "description": "Prueba de upload.",
            "document_file": (
                BytesIO(b"%PDF-1.4 test"),
                "manual_test.pdf",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    stored_name = (
        "TEST-PDF-001__manual_test.pdf"
    )

    assert test_storage.exists(
        stored_name
    ) is True

    document = documents_test_db.get_by_code(
        "TEST-PDF-001"
    )

    assert document is not None
    assert document.file_name == stored_name


def test_view_document_should_return_pdf(
    authenticated_client,
    documents_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.documents.storage import (
        LocalDocumentStorage,
    )

    test_storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    monkeypatch.setattr(
        routes,
        "document_storage",
        test_storage,
    )

    # Crear y subir un PDF mediante HTTP.
    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-PDF-VIEW-001",
            "title": "PDF para visualizar",
            "document_type": "manual",
            "revision": "A",
            "description": "Prueba de visualización.",
            "document_file": (
                BytesIO(b"%PDF-1.4 test view"),
                "view_test.pdf",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    # Solicitar el PDF desde la nueva ruta.
    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/"
            "TEST-PDF-VIEW-001/"
            "ver"
        )
    )

    assert response.status_code == 200

    assert (
        response.mimetype
        == "application/pdf"
    )

    assert response.data.startswith(
        b"%PDF-1.4"
    )

def test_delete_document_should_remove_pdf_file(
    authenticated_client,
    documents_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.documents.storage import (
        LocalDocumentStorage,
    )

    test_storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    monkeypatch.setattr(
        routes,
        "document_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-PDF-DELETE-001",
            "title": "PDF para eliminar",
            "document_type": "manual",
            "revision": "A",
            "description": "Prueba delete físico.",
            "document_file": (
                BytesIO(b"%PDF-1.4 delete test"),
                "delete_test.pdf",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    stored_name = (
        "TEST-PDF-DELETE-001__delete_test.pdf"
    )

    assert test_storage.exists(
        stored_name
    ) is True

    document = documents_test_db.get_by_code(
        "TEST-PDF-DELETE-001"
    )

    assert document is not None

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/"
            "TEST-PDF-DELETE-001/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert documents_test_db.get_by_code(
        "TEST-PDF-DELETE-001"
    ) is None

    assert test_storage.exists(
        stored_name
    ) is False

def test_upload_non_pdf_should_be_rejected(
   authenticated_client,
    documents_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.documents.storage import (
        LocalDocumentStorage,
    )

    test_storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    monkeypatch.setattr(
        routes,
        "document_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "documentos/nuevo"
        ),
        data={
            "code": "TEST-NON-PDF-001",
            "title": "Archivo no permitido",
            "document_type": "manual",
            "revision": "A",
            "description": "Debe ser rechazado.",
            "document_file": (
                BytesIO(b"archivo de texto"),
                "archivo.txt",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 400

    assert documents_test_db.get_by_code(
        "TEST-NON-PDF-001"
    ) is None

    assert test_storage.exists(
        "TEST-NON-PDF-001__archivo.txt"
    ) is False

def test_create_photo_form_should_respond(
    authenticated_client,
) -> None:

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        )
    )

    assert response.status_code == 200

    assert (
        "Registrar fotografía"
        in response.get_data(as_text=True)
    )


def test_upload_image_should_persist_photo(
    authenticated_client,
    photos_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.photos.storage import (
        LocalPhotoStorage,
    )

    test_storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    monkeypatch.setattr(
        routes,
        "photo_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        ),
        data={
            "code": "TEST-PHOTO-HTTP-001",
            "title": "Foto general de prueba",
            "photo_type": "general",
            "description": (
                "Fotografía creada mediante "
                "una prueba HTTP."
            ),
            "photo_file": (
                BytesIO(
                    b"fake jpeg image data"
                ),
                "equipo_test.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    stored_name = (
        "TEST-PHOTO-HTTP-001__equipo_test.jpg"
    )

    assert test_storage.exists(
        stored_name
    ) is True

    photo = photos_test_db.get_by_code(
        "TEST-PHOTO-HTTP-001"
    )

    assert photo is not None

    assert (
        photo.asset_code
        == "S2-480-ES09-T269"
    )

    assert (
        photo.title
        == "Foto general de prueba"
    )

    assert photo.photo_type == "general"

    assert photo.file_name == stored_name

def test_view_photo_should_return_image(
    authenticated_client,
    photos_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.photos.storage import (
        LocalPhotoStorage,
    )

    test_storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    monkeypatch.setattr(
        routes,
        "photo_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        ),
        data={
            "code": "TEST-PHOTO-VIEW-001",
            "title": "Foto para visualizar",
            "photo_type": "general",
            "description": "Prueba de visualización.",
            "photo_file": (
                BytesIO(
                    b"fake jpeg image view data"
                ),
                "view_test.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/"
            "TEST-PHOTO-VIEW-001/"
            "ver"
        )
    )

    assert response.status_code == 200

    assert response.mimetype == "image/jpeg"

    assert response.data == (
        b"fake jpeg image view data"
    )


def test_upload_non_image_should_be_rejected(
    authenticated_client,
    photos_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.photos.storage import (
        LocalPhotoStorage,
    )

    test_storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    monkeypatch.setattr(
        routes,
        "photo_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        ),
        data={
            "code": "TEST-NON-IMAGE-001",
            "title": "Archivo no permitido",
            "photo_type": "general",
            "description": "Debe ser rechazado.",
            "photo_file": (
                BytesIO(
                    b"archivo de texto"
                ),
                "archivo.txt",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 400

    assert photos_test_db.get_by_code(
        "TEST-NON-IMAGE-001"
    ) is None

    assert test_storage.exists(
        "TEST-NON-IMAGE-001__archivo.txt"
    ) is False

def test_edit_photo_should_update_and_redirect(
    authenticated_client,
    photos_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.photos.storage import (
        LocalPhotoStorage,
    )

    test_storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    monkeypatch.setattr(
        routes,
        "photo_storage",
        test_storage,
    )

    # Crear primero una fotografía real.
    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        ),
        data={
            "code": "TEST-PHOTO-EDIT-001",
            "title": "Foto original",
            "photo_type": "general",
            "description": "Versión original.",
            "photo_file": (
                BytesIO(
                    b"fake image edit data"
                ),
                "edit_test.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    original = photos_test_db.get_by_code(
        "TEST-PHOTO-EDIT-001"
    )

    assert original is not None

    original_file_name = original.file_name

    # Editar únicamente metadata.
    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/"
            "TEST-PHOTO-EDIT-001/"
            "editar"
        ),
        data={
            "title": "Foto actualizada",
            "photo_type": "nameplate",
            "description": "Descripción actualizada.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = photos_test_db.get_by_code(
        "TEST-PHOTO-EDIT-001"
    )

    assert persisted is not None

    assert persisted.title == "Foto actualizada"
    assert persisted.photo_type == "nameplate"
    assert (
        persisted.description
        == "Descripción actualizada."
    )

    # La edición de metadata no reemplaza el archivo.
    assert (
        persisted.file_name
        == original_file_name
    )

    assert test_storage.exists(
        original_file_name
    ) is True


def test_delete_photo_should_remove_image_file(
    authenticated_client,
    photos_test_db,
    tmp_path,
    monkeypatch,
) -> None:

    from app.assets import routes

    from app.domains.assets.photos.storage import (
        LocalPhotoStorage,
    )

    test_storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    monkeypatch.setattr(
        routes,
        "photo_storage",
        test_storage,
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/nueva"
        ),
        data={
            "code": "TEST-PHOTO-DELETE-001",
            "title": "Foto para eliminar",
            "photo_type": "general",
            "description": "Prueba de eliminación.",
            "photo_file": (
                BytesIO(
                    b"fake image delete data"
                ),
                "delete_photo.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302

    photo = photos_test_db.get_by_code(
        "TEST-PHOTO-DELETE-001"
    )

    assert photo is not None

    stored_name = photo.file_name

    assert test_storage.exists(
        stored_name
    ) is True

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "fotografias/"
            "TEST-PHOTO-DELETE-001/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert photos_test_db.get_by_code(
        "TEST-PHOTO-DELETE-001"
    ) is None

    assert test_storage.exists(
        stored_name
    ) is False

def test_create_maintenance_event_form_should_respond(
    authenticated_client,
) -> None:

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "mantenimiento/nuevo"
        )
    )

    assert response.status_code == 200

    assert (
        "Registrar mantenimiento"
        in response.get_data(as_text=True)
    )


def test_create_maintenance_event_should_persist_and_redirect(
    authenticated_client,
    maintenance_history_test_db,
) -> None:

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "mantenimiento/nuevo"
        ),
        data={
            "code": "ME-HTTP-001",
            "event_type": "inspection",
            "title": "Inspección general",
            "performed_by": "Fortunato Tenorio",
            "started_at": "2026-08-10T16:00",
            "completed_at": "",
            "description": "Revisión general.",
            "observations": "Sin anomalías.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    event = (
        maintenance_history_test_db.get_by_code(
            "ME-HTTP-001"
        )
    )

    assert event is not None

    assert (
        event.asset_code
        == "S2-480-ES09-T269"
    )

    assert event.event_type == "inspection"
    assert event.title == "Inspección general"
    assert event.is_completed is False


def test_create_maintenance_event_should_reject_invalid_date(
    authenticated_client,
    maintenance_history_test_db,
) -> None:

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "mantenimiento/nuevo"
        ),
        data={
            "code": "ME-HTTP-BAD-DATE",
            "event_type": "inspection",
            "title": "Inspección",
            "performed_by": "Fortunato Tenorio",
            "started_at": "fecha-invalida",
            "completed_at": "",
            "description": "Prueba.",
            "observations": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    assert (
        maintenance_history_test_db.get_by_code(
            "ME-HTTP-BAD-DATE"
        )
        is None
    )

def test_edit_maintenance_event_should_update_and_redirect(
    authenticated_client,
    maintenance_history_test_db,
) -> None:

    maintenance_history_test_db.save(
        MaintenanceEvent(
            code="ME-HTTP-EDIT-001",
            asset_code="S2-480-ES09-T269",
            event_type="inspection",
            title="Inspección inicial",
            description="Revisión inicial.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                10,
                8,
                0,
            ),
        )
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "mantenimiento/"
            "ME-HTTP-EDIT-001/"
            "editar"
        ),
        data={
            "event_type": "corrective",
            "title": "Mantenimiento terminado",
            "performed_by": "Fortunato Tenorio",
            "started_at": "2026-08-10T08:00",
            "completed_at": "2026-08-10T10:30",
            "description": "Se realizó reparación.",
            "observations": "Equipo liberado.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    event = (
        maintenance_history_test_db.get_by_code(
            "ME-HTTP-EDIT-001"
        )
    )

    assert event is not None
    assert event.event_type == "corrective"

    assert (
        event.title
        == "Mantenimiento terminado"
    )

    assert event.completed_at is not None
    assert event.is_completed is True

    assert (
        event.observations
        == "Equipo liberado."
    )


def test_delete_maintenance_event_should_remove_and_redirect(
    authenticated_client,
    maintenance_history_test_db,
) -> None:

    maintenance_history_test_db.save(
        MaintenanceEvent(
            code="ME-HTTP-DELETE-001",
            asset_code="S2-480-ES09-T269",
            event_type="inspection",
            title="Evento para eliminar",
            description="Prueba.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                10,
                9,
                0,
            ),
        )
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "mantenimiento/"
            "ME-HTTP-DELETE-001/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    event = (
        maintenance_history_test_db.get_by_code(
            "ME-HTTP-DELETE-001"
        )
    )

    assert event is None

def test_people_index_should_respond(
    authenticated_client,
    people_test_db,
) -> None:

    response = authenticated_client.get(
        "/personas"
    )

    assert response.status_code == 200

    assert (
        "Personas"
        in response.get_data(as_text=True)
    )


def test_create_person_should_persist_and_redirect(
    authenticated_client,
    people_test_db,
) -> None:

    response = authenticated_client.post(
        "/personas/nueva",
        data={
            "code": "TECH-HTTP-001",
            "name": "Angel",
            "position": "Técnico",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    person = people_test_db.get_by_code(
        "TECH-HTTP-001"
    )

    assert person is not None
    assert person.name == "Angel"
    assert person.position == "Técnico"
    assert person.is_active is True


def test_edit_person_should_update_and_redirect(
    authenticated_client,
    people_test_db,
) -> None:

    from app.domains.identity.people.entities import (
        Person,
    )

    people_test_db.save(
        Person(
            code="TECH-HTTP-EDIT-001",
            name="Angel",
            position="Técnico",
        )
    )

    response = authenticated_client.post(
        (
            "/personas/"
            "TECH-HTTP-EDIT-001/"
            "editar"
        ),
        data={
            "name": "Angel Updated",
            "position": "Técnico Senior",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    person = people_test_db.get_by_code(
        "TECH-HTTP-EDIT-001"
    )

    assert person is not None
    assert person.name == "Angel Updated"
    assert person.position == "Técnico Senior"


def test_toggle_person_status_should_persist(
    authenticated_client,
    people_test_db,
) -> None:

    from app.domains.identity.people.entities import (
        Person,
    )

    people_test_db.save(
        Person(
            code="TECH-HTTP-STATUS-001",
            name="Daniel",
            position="Técnico",
        )
    )

    response = authenticated_client.post(
        (
            "/personas/"
            "TECH-HTTP-STATUS-001/"
            "estado"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    person = people_test_db.get_by_code(
        "TECH-HTTP-STATUS-001"
    )

    assert person is not None
    assert person.is_active is False

    response = authenticated_client.post(
        (
            "/personas/"
            "TECH-HTTP-STATUS-001/"
            "estado"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    person = people_test_db.get_by_code(
        "TECH-HTTP-STATUS-001"
    )

    assert person is not None
    assert person.is_active is True



def test_roles_index_should_respond(
    authenticated_client,
    roles_test_db,
) -> None:

    response = authenticated_client.get(
        "/roles"
    )

    assert response.status_code == 200

    assert (
        "Roles"
        in response.get_data(as_text=True)
    )


def test_create_role_should_persist_and_redirect(
    authenticated_client,
    roles_test_db,
) -> None:

    response = authenticated_client.post(
        "/roles/nuevo",
        data={
            "code": "SUPERVISOR",
            "name": "Supervisor",
            "description": (
                "Supervisor de mantenimiento"
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    role = roles_test_db.get_by_code(
        "SUPERVISOR"
    )

    assert role is not None
    assert role.code == "SUPERVISOR"
    assert role.name == "Supervisor"
    assert (
        role.description
        == "Supervisor de mantenimiento"
    )
    assert role.is_active is True


def test_edit_role_should_update_and_redirect(
    authenticated_client,
    roles_test_db,
) -> None:

    from app.domains.identity.roles.entities import (
        Role,
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
            description="Rol técnico",
        )
    )

    response = authenticated_client.post(
        "/roles/TECHNICIAN/editar",
        data={
            "name": "Técnico Senior",
            "description": (
                "Rol técnico actualizado"
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    role = roles_test_db.get_by_code(
        "TECHNICIAN"
    )

    assert role is not None
    assert role.name == "Técnico Senior"
    assert (
        role.description
        == "Rol técnico actualizado"
    )


def test_toggle_role_status_should_persist(
    authenticated_client,
    roles_test_db,
) -> None:

    from app.domains.identity.roles.entities import (
        Role,
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    response = authenticated_client.post(
        "/roles/TECHNICIAN/estado",
        follow_redirects=False,
    )

    assert response.status_code == 302

    role = roles_test_db.get_by_code(
        "TECHNICIAN"
    )

    assert role is not None
    assert role.is_active is False

    response = authenticated_client.post(
        "/roles/TECHNICIAN/estado",
        follow_redirects=False,
    )

    assert response.status_code == 302

    role = roles_test_db.get_by_code(
        "TECHNICIAN"
    )

    assert role is not None
    assert role.is_active is True


def test_create_user_should_hash_password(
    authenticated_client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import (
        Person,
    )

    from app.domains.identity.roles.entities import (
        Role,
    )

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    plain_password = "Secret123"

    response = authenticated_client.post(
        "/usuarios/nuevo",
        data={
            "username": "angel",
            "password": plain_password,
            "person_code": "TECH-001",
            "role_code": "TECHNICIAN",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    user = users_test_db.get_by_username(
        "angel"
    )

    assert user is not None

    assert (
        user.password_hash
        != plain_password
    )

    assert password_hasher.verify(
        plain_password,
        user.password_hash,
    ) is True

def test_edit_user_should_preserve_password_hash(
    authenticated_client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import (
        Person,
    )

    from app.domains.identity.roles.entities import (
        Role,
    )

    from app.domains.identity.users.entities import (
        User,
    )

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    people_test_db.save(
        Person(
            code="TECH-002",
            name="Daniel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    roles_test_db.save(
        Role(
            code="SUPERVISOR",
            name="Supervisor",
        )
    )

    original_hash = password_hasher.hash(
        "Secret123"
    )

    users_test_db.save(
        User(
            username="angel",
            password_hash=original_hash,
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    response = authenticated_client.post(
        "/usuarios/angel/editar",
        data={
            "person_code": "TECH-002",
            "role_code": "SUPERVISOR",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    user = users_test_db.get_by_username(
        "angel"
    )

    assert user is not None

    assert (
        user.password_hash
        == original_hash
    )

    assert (
        user.person_code
        == "TECH-002"
    )

    assert (
        user.role_code
        == "SUPERVISOR"
    )

    assert password_hasher.verify(
        "Secret123",
        user.password_hash,
    ) is True


def test_toggle_user_status_should_preserve_identity_data(
    authenticated_client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import (
        Person,
    )

    from app.domains.identity.roles.entities import (
        Role,
    )

    from app.domains.identity.users.entities import (
        User,
    )

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    password_hash = password_hasher.hash(
        "Secret123"
    )

    users_test_db.save(
        User(
            username="angel",
            password_hash=password_hash,
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    response = authenticated_client.post(
        "/usuarios/angel/estado",
        follow_redirects=False,
    )

    assert response.status_code == 302

    user = users_test_db.get_by_username(
        "angel"
    )

    assert user is not None
    assert user.is_active is False

    assert user.username == "angel"
    assert user.person_code == "TECH-001"
    assert user.role_code == "TECHNICIAN"

    assert (
        user.password_hash
        == password_hash
    )

    response = authenticated_client.post(
        "/usuarios/angel/estado",
        follow_redirects=False,
    )

    assert response.status_code == 302

    user = users_test_db.get_by_username(
        "angel"
    )

    assert user is not None
    assert user.is_active is True



def test_login_should_create_session(
    client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import Person
    from app.domains.identity.roles.entities import Role
    from app.domains.identity.users.entities import User

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    password_hash = password_hasher.hash(
        "Secret123"
    )

    users_test_db.save(
        User(
            username="angel",
            password_hash=password_hash,
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    response = client.post(
        "/login",
        data={
            "username": "angel",
            "password": "Secret123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session["username"] == "angel"
        assert session["person_code"] == "TECH-001"
        assert session["role_code"] == "TECHNICIAN"


def test_login_should_reject_invalid_password(
    client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import Person
    from app.domains.identity.roles.entities import Role
    from app.domains.identity.users.entities import User

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    users_test_db.save(
        User(
            username="angel",
            password_hash=password_hasher.hash(
                "Secret123"
            ),
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    response = client.post(
        "/login",
        data={
            "username": "angel",
            "password": "WrongPassword",
        },
        follow_redirects=False,
    )

    assert response.status_code == 401

    with client.session_transaction() as session:
        assert "username" not in session


def test_login_should_reject_inactive_user(
    client,
    users_test_db,
    people_test_db,
    roles_test_db,
) -> None:

    from app.domains.identity.people.entities import Person
    from app.domains.identity.roles.entities import Role
    from app.domains.identity.users.entities import User

    people_test_db.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    roles_test_db.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    users_test_db.save(
        User(
            username="angel",
            password_hash=password_hasher.hash(
                "Secret123"
            ),
            person_code="TECH-001",
            role_code="TECHNICIAN",
            is_active=False,
        )
    )

    response = client.post(
        "/login",
        data={
            "username": "angel",
            "password": "Secret123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 401

    with client.session_transaction() as session:
        assert "username" not in session


def test_logout_should_clear_session(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/logout",
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "username" not in session
        assert "person_code" not in session
        assert "role_code" not in session



def test_people_index_should_require_login(
    client,
) -> None:

    response = client.get(
        "/personas",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )


def test_roles_index_should_require_login(
    client,
) -> None:

    response = client.get(
        "/roles",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )


def test_users_index_should_require_login(
    client,
) -> None:

    response = client.get(
        "/usuarios",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )

def test_admin_should_access_users(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/usuarios"
    )

    assert response.status_code == 200


def test_technician_should_not_access_users(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/usuarios"
    )

    assert response.status_code == 403

def test_admin_should_access_roles(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/roles"
    )

    assert response.status_code == 200


def test_technician_should_not_access_roles(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/roles"
    )

    assert response.status_code == 403

def test_admin_should_access_people(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/personas"
    )

    assert response.status_code == 200


def test_supervisor_should_access_people(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["person_code"] = "SUP-001"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/personas"
    )

    assert response.status_code == 200


def test_technician_should_not_access_people(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/personas"
    )

    assert response.status_code == 403


def test_technician_should_access_assets(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200


def test_unknown_role_should_not_access_assets(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "unknown"
        session["person_code"] = "UNKNOWN-001"
        session["role_code"] = "UNKNOWN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 403

def test_admin_should_manage_documents(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 200


def test_supervisor_should_manage_documents(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["person_code"] = "SUP-001"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 200


def test_manager_should_not_manage_documents(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["person_code"] = "MGR-001"
        session["role_code"] = "MANAGER"

    response = client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 403


def test_technician_should_not_manage_documents(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 403

def test_admin_should_manage_photos(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activo/S2-480-ES09-T269/fotografias/nueva"
    )

    assert response.status_code == 200


def test_supervisor_should_manage_photos(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["person_code"] = "SUP-001"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/activo/S2-480-ES09-T269/fotografias/nueva"
    )

    assert response.status_code == 200


def test_manager_should_not_manage_photos(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["person_code"] = "MGR-001"
        session["role_code"] = "MANAGER"

    response = client.get(
        "/activo/S2-480-ES09-T269/fotografias/nueva"
    )

    assert response.status_code == 403


def test_technician_should_not_manage_photos(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activo/S2-480-ES09-T269/fotografias/nueva"
    )

    assert response.status_code == 403

def test_admin_should_manage_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activo/S2-480-ES09-T269/mantenimiento/nuevo"
    )

    assert response.status_code == 200


def test_supervisor_should_manage_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["person_code"] = "SUP-001"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/activo/S2-480-ES09-T269/mantenimiento/nuevo"
    )

    assert response.status_code == 200


def test_technician_should_manage_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activo/S2-480-ES09-T269/mantenimiento/nuevo"
    )

    assert response.status_code == 200


def test_manager_should_not_manage_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["person_code"] = "MGR-001"
        session["role_code"] = "MANAGER"

    response = client.get(
        "/activo/S2-480-ES09-T269/mantenimiento/nuevo"
    )

    assert response.status_code == 403


def test_create_preventive_maintenance_form_should_respond(
    authenticated_client,
) -> None:

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        )
    )

    assert response.status_code == 200

    assert (
        "Registrar plan preventivo"
        in response.get_data(
            as_text=True
        )
    )

def test_create_preventive_maintenance_should_persist_and_redirect(
    authenticated_client,
    preventive_maintenance_test_db,
) -> None:

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        ),
        data={
            "code": "PM-HTTP-001",
            "title": "Inspección trimestral",
            "frequency_days": "90",
            "responsible_person_code": "55464",
            "next_due_at": "2026-09-01T08:00",
            "description": (
                "Inspección preventiva general."
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    plan = (
        preventive_maintenance_test_db
        .get_by_code(
            "PM-HTTP-001"
        )
    )

    assert plan is not None

    assert (
        plan.asset_code
        == "S2-480-ES09-T269"
    )

    assert (
        plan.title
        == "Inspección trimestral"
    )

    assert plan.frequency_days == 90

    assert (
        plan.responsible_person_code
        == "55464"
    )

    assert plan.is_active is True


def test_preventive_maintenance_should_require_login(
    client,
) -> None:

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )


def test_admin_should_manage_preventive_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        )
    )

    assert response.status_code == 200


def test_supervisor_should_manage_preventive_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["person_code"] = "SUP-001"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        )
    )

    assert response.status_code == 200


def test_technician_should_not_manage_preventive_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "technician"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        )
    )

    assert response.status_code == 403


def test_manager_should_not_manage_preventive_maintenance(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["person_code"] = "MGR-001"
        session["role_code"] = "MANAGER"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/nuevo"
        )
    )

    assert response.status_code == 403

def test_edit_preventive_maintenance_form_should_respond(
    authenticated_client,
    preventive_maintenance_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    preventive_maintenance_test_db.save(
        PreventiveMaintenancePlan(
            code="PM-EDIT-001",
            asset_code="S2-480-ES09-T269",
            title="Plan original",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            description="Original.",
        )
    )

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-EDIT-001/"
            "editar"
        )
    )

    assert response.status_code == 200

    assert (
        "Editar plan preventivo"
        in response.get_data(
            as_text=True
        )
    )


def test_edit_preventive_maintenance_should_update_and_redirect(
    authenticated_client,
    preventive_maintenance_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    preventive_maintenance_test_db.save(
        PreventiveMaintenancePlan(
            code="PM-EDIT-002",
            asset_code="S2-480-ES09-T269",
            title="Plan original",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            description="Original.",
        )
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-EDIT-002/"
            "editar"
        ),
        data={
            "title": "Plan actualizado",
            "frequency_days": "60",
            "responsible_person_code": "55464",
            "next_due_at": "2026-10-15T09:30",
            "description": "Actualizado.",
            "is_active": "on",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = (
        preventive_maintenance_test_db
        .get_by_code(
            "PM-EDIT-002"
        )
    )

    assert persisted is not None
    assert persisted.title == "Plan actualizado"
    assert persisted.frequency_days == 60
    assert persisted.description == "Actualizado."
    assert persisted.is_active is True


def test_technician_should_not_edit_preventive_maintenance(
    client,
    preventive_maintenance_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    preventive_maintenance_test_db.save(
        PreventiveMaintenancePlan(
            code="PM-EDIT-003",
            asset_code="S2-480-ES09-T269",
            title="Plan técnico",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "technician"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-EDIT-003/"
            "editar"
        )
    )

    assert response.status_code == 403

def test_delete_preventive_maintenance_should_remove_and_redirect(
    authenticated_client,
    preventive_maintenance_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    preventive_maintenance_test_db.save(
        PreventiveMaintenancePlan(
            code="PM-DELETE-001",
            asset_code="S2-480-ES09-T269",
            title="Plan para eliminar",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-DELETE-001/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = (
        preventive_maintenance_test_db
        .get_by_code(
            "PM-DELETE-001"
        )
    )

    assert persisted is None


def test_delete_unknown_preventive_maintenance_should_return_404(
    authenticated_client,
    preventive_maintenance_test_db,
) -> None:

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-NOT-FOUND/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_technician_should_not_delete_preventive_maintenance(
    client,
    preventive_maintenance_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    preventive_maintenance_test_db.save(
        PreventiveMaintenancePlan(
            code="PM-DELETE-TECH-001",
            asset_code="S2-480-ES09-T269",
            title="Plan protegido",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "technician"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-DELETE-TECH-001/"
            "eliminar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 403

    persisted = (
        preventive_maintenance_test_db
        .get_by_code(
            "PM-DELETE-TECH-001"
        )
    )

    assert persisted is not None


def test_complete_preventive_maintenance_form_should_respond(
    authenticated_client,
    preventive_execution_web_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    plan_repository, _ = (
        preventive_execution_web_test_db
    )

    plan_repository.save(
        PreventiveMaintenancePlan(
            code="PM-COMPLETE-001",
            asset_code="S2-480-ES09-T269",
            title="Inspección trimestral",
            frequency_days=90,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
        )
    )

    response = authenticated_client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-COMPLETE-001/"
            "completar"
        )
    )

    assert response.status_code == 200

    assert (
        "Completar preventivo"
        in response.get_data(
            as_text=True
        )
    )


def test_complete_preventive_maintenance_should_persist_and_reschedule(
    authenticated_client,
    preventive_execution_web_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    (
        plan_repository,
        execution_repository,
    ) = preventive_execution_web_test_db

    plan_repository.save(
        PreventiveMaintenancePlan(
            code="PM-COMPLETE-002",
            asset_code="S2-480-ES09-T269",
            title="Inspección trimestral",
            frequency_days=90,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
        )
    )

    response = authenticated_client.post(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-COMPLETE-002/"
            "completar"
        ),
        data={
            "execution_code": "PME-WEB-001",
            "performed_by": "Fortunato Tenorio",
            "completed_at": "2026-09-01T10:00",
            "observations": "Sin anomalías.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    execution = (
        execution_repository.get_by_code(
            "PME-WEB-001"
        )
    )

    assert execution is not None

    assert (
        execution.plan_code
        == "PM-COMPLETE-002"
    )

    plan = plan_repository.get_by_code(
        "PM-COMPLETE-002"
    )

    assert plan is not None

    assert (
        plan.next_due_at
        == datetime(
            2026,
            11,
            30,
            10,
            0,
        )
    )

def test_technician_should_execute_preventive_maintenance(
    client,
    preventive_execution_web_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    plan_repository, _ = (
        preventive_execution_web_test_db
    )

    plan_repository.save(
        PreventiveMaintenancePlan(
            code="PM-TECH-EXEC-001",
            asset_code="S2-480-ES09-T269",
            title="Preventivo técnico",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "technician"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-TECH-EXEC-001/"
            "completar"
        )
    )

    assert response.status_code == 200

def test_manager_should_not_execute_preventive_maintenance(
    client,
    preventive_execution_web_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenancePlan,
    )

    plan_repository, _ = (
        preventive_execution_web_test_db
    )

    plan_repository.save(
        PreventiveMaintenancePlan(
            code="PM-MANAGER-EXEC-001",
            asset_code="S2-480-ES09-T269",
            title="Preventivo protegido",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["person_code"] = "MGR-001"
        session["role_code"] = "MANAGER"

    response = client.get(
        (
            "/activo/"
            "S2-480-ES09-T269/"
            "preventivo/"
            "PM-MANAGER-EXEC-001/"
            "completar"
        )
    )

    assert response.status_code == 403


def test_asset_detail_should_show_preventive_execution(
    authenticated_client,
    preventive_execution_web_test_db,
) -> None:

    from datetime import datetime

    from app.domains.assets.preventive_maintenance.entities import (
        PreventiveMaintenanceExecution,
    )

    _, execution_repository = (
        preventive_execution_web_test_db
    )

    execution_repository.save(
        PreventiveMaintenanceExecution(
            code="PME-VIEW-001",
            plan_code="PM-VIEW-001",
            asset_code="S2-480-ES09-T269",
            performed_by="Fortunato Tenorio",
            scheduled_at=datetime(
                2026,
                8,
                14,
                18,
                0,
            ),
            completed_at=datetime(
                2026,
                8,
                14,
                19,
                4,
            ),
            observations="Inspección terminada.",
        )
    )

    response = authenticated_client.get(
        "/activo/S2-480-ES09-T269"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Ejecuciones preventivas" in html
    assert "PME-VIEW-001" in html
    assert "PM-VIEW-001" in html
    assert "Fortunato Tenorio" in html
    assert "Inspección terminada." in html

def test_asset_detail_should_show_empty_preventive_execution_message(
    authenticated_client,
    preventive_execution_web_test_db,
) -> None:

    response = authenticated_client.get(
        "/activo/S2-480-ES09-T269"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        "Todavía no hay ejecuciones preventivas"
        in html
    )