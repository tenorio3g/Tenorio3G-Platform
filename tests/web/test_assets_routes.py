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
def test_asset_edit_form_should_allow_missing_installation_date(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-NO-DATE",
            name="Panel Edit No Date",
            model_number="EDIT-NO-DATE",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para activo sin fecha."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-NO-DATE",
            name="Ubicacion Edit No Date",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-NO-DATE",
            name="Tablero Sin Fecha",
            asset_model_code=(
                "PANEL-EDIT-NO-DATE"
            ),
            serial_number="",
            location_code=(
                "LOC-EDIT-NO-DATE"
            ),
            status=AssetStatus.OPERATING,
            installation_date=None,
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/T-EDIT-NO-DATE/editar"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Editar activo" in html
    assert "T-EDIT-NO-DATE" in html
    assert 'value="Tablero Sin Fecha"' in html
    assert 'name="installation_date"' in html

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

def test_asset_models_index_should_respond_for_authorized_user(
    authenticated_client,
) -> None:

    response = authenticated_client.get(
        "/activos/modelos"
    )

    assert response.status_code == 200

    assert (
        b"TAB-480-01"
        in response.data
    )

def test_asset_models_index_should_reject_role_without_assets_view(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "unknown"
        session["person_code"] = "UNKNOWN-001"
        session["role_code"] = "UNKNOWN"

    response = client.get(
        "/activos/modelos"
    )

    assert response.status_code == 403


def test_admin_should_open_new_asset_model_form(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/modelos/nuevo"
    )

    assert response.status_code == 200


def test_technician_should_not_open_new_asset_model_form(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activos/modelos/nuevo"
    )

    assert response.status_code == 403


def test_admin_should_create_asset_model(
    client,
    asset_models_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/modelos/nuevo",
        data={
            "code": "MOTOR-TEST-01",
            "name": "Motor de prueba",
            "model_number": "MTR-100",
            "manufacturer_code": "TEST-MANUFACTURER",
            "asset_type_code": "MOTOR",
            "description": "Modelo creado desde la interfaz web.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/activos/modelos"
    )

    saved_model = (
        asset_models_test_db.find_by_code(
            "MOTOR-TEST-01"
        )
    )

    assert saved_model is not None
    assert saved_model.code == "MOTOR-TEST-01"
    assert saved_model.name == "Motor de prueba"
    assert saved_model.model_number == "MTR-100"
    assert (
        saved_model.manufacturer_code
        == "TEST-MANUFACTURER"
    )
    assert (
        saved_model.asset_type_code
        == "MOTOR"
    )

    saved_model = (
        asset_models_test_db.find_by_code(
            "MOTOR-TEST-01"
        )
    )

    assert saved_model is not None
    assert saved_model.code == "MOTOR-TEST-01"
    assert saved_model.name == "Motor de prueba"
    assert saved_model.model_number == "MTR-100"
    assert (
        saved_model.manufacturer_code
        == "TEST-MANUFACTURER"
    )
    assert (
        saved_model.asset_type_code
        == "MOTOR"
    )


def test_admin_should_not_create_duplicate_asset_model(
    client,
    asset_models_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    payload = {
        "code": "MOTOR-TEST-01",
        "name": "Motor de prueba",
        "model_number": "MTR-100",
        "manufacturer_code": "TEST-MANUFACTURER",
        "asset_type_code": "MOTOR",
        "description": "Modelo creado desde la interfaz web.",
    }

    first_response = client.post(
        "/activos/modelos/nuevo",
        data=payload,
        follow_redirects=False,
    )

    second_response = client.post(
        "/activos/modelos/nuevo",
        data=payload,
        follow_redirects=False,
    )

    assert first_response.status_code == 302
    assert second_response.status_code == 400

    saved_models = (
        asset_models_test_db.find_all()
    )

    matching_models = [
        asset_model
        for asset_model in saved_models
        if asset_model.code == "MOTOR-TEST-01"
    ]

    assert len(matching_models) == 1

    assert (
        b"Ya existe un modelo"
        in second_response.data
    )

    assert (
        b'value="MOTOR-TEST-01"'
        in second_response.data
    )

    assert (
        b'value="MTR-100"'
        in second_response.data
    )

    assert (
        b"Modelo creado desde la interfaz web."
        in second_response.data
    )


def test_admin_should_see_new_asset_model_action(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/modelos"
    )

    assert response.status_code == 200

    assert (
        b"/activos/modelos/nuevo"
        in response.data
    )

    assert (
        b"Nuevo modelo"
        in response.data
    )


def test_technician_should_not_see_new_asset_model_action(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activos/modelos"
    )

    assert response.status_code == 200

    assert (
        b"/activos/modelos/nuevo"
        not in response.data
    )

    assert (
        b"Nuevo modelo"
        not in response.data
    )


def test_admin_should_open_new_asset_form(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200


def test_new_asset_form_should_list_persistent_asset_models(
    client,
    asset_models_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )

    asset_models_test_db.save(
        AssetModel(
            code="MOTOR-FORM-01",
            name="Motor para formulario",
            model_number="MTR-FORM",
            manufacturer_code="TEST-MANUFACTURER",
            asset_type_code="MOTOR",
            description="Modelo de prueba para formulario.",
            specifications={},
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    assert (
        b'MOTOR-FORM-01'
        in response.data
    )

    assert (
        b'Motor para formulario'
        in response.data
    )

    assert (
        b'value="MOTOR-FORM-01"'
        in response.data
    )



def test_new_asset_form_should_list_only_active_physical_locations(
    client,
    assets_test_db,
) -> None:

    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    location_repository.save(
        PhysicalLocation(
            code="PLANTA-ACTIVA",
            name="Planta Activa",
            area="PLANTA",
            is_active=True,
        )
    )

    location_repository.save(
        PhysicalLocation(
            code="PLANTA-INACTIVA",
            name="Planta Inactiva",
            area="PLANTA",
            is_active=False,
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    assert (
        b"PLANTA-ACTIVA"
        in response.data
    )

    assert (
        b"Planta Activa"
        in response.data
    )

    assert (
        b"PLANTA-INACTIVA"
        not in response.data
    )

    assert (
        b"Planta Inactiva"
        not in response.data
    )


def test_admin_should_create_asset(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="PLANTA-01",
            name="Planta 01",
            area="PLANTA",
        )
    )

    asset_model_repository.save(
        AssetModel(
            code="MOTOR-01",
            name="Motor 10 HP",
            model_number="MTR-10HP",
            manufacturer_code="TEST",
            asset_type_code="MOTOR",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "MOTOR-PLANTA-01",
            "name": "Motor bomba 1",
            "asset_model_code": "MOTOR-01",
            "serial_number": "SN-001",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers["Location"].endswith(
        "/activos"
    )

    saved_asset = (
        asset_repository.find_by_code(
            "MOTOR-PLANTA-01"
        )
    )

    assert saved_asset is not None
    assert saved_asset.code == (
        "MOTOR-PLANTA-01"
    )
    assert saved_asset.name == (
        "Motor bomba 1"
    )
    assert saved_asset.asset_model_code == (
        "MOTOR-01"
    )
    assert saved_asset.location_code == (
        "PLANTA-01"
    )


def test_admin_should_not_create_duplicate_asset(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="PLANTA-01",
            name="Planta 01",
            area="PLANTA",
        )
    )

    asset_model_repository.save(
        AssetModel(
            code="MOTOR-01",
            name="Motor 10 HP",
            model_number="MTR-10HP",
            manufacturer_code="TEST",
            asset_type_code="MOTOR",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    payload = {
        "code": "MOTOR-PLANTA-01",
        "name": "Motor bomba 1",
        "asset_model_code": "MOTOR-01",
        "serial_number": "SN-001",
        "location_code": "PLANTA-01",
        "status": "OPERATING",
        "installation_date": "2026-08-30",
    }

    first_response = client.post(
        "/activos/nuevo",
        data=payload,
        follow_redirects=False,
    )

    second_response = client.post(
        "/activos/nuevo",
        data=payload,
        follow_redirects=False,
    )

    assert first_response.status_code == 302
    assert second_response.status_code == 400

    saved_assets = (
        asset_repository.find_all()
    )

    matching_assets = [
        asset
        for asset in saved_assets
        if asset.code == "MOTOR-PLANTA-01"
    ]

    assert len(matching_assets) == 1

    assert (
        b"Ya existe"
        in second_response.data
    )

    assert (
        b'value="MOTOR-PLANTA-01"'
        in second_response.data
    )

    assert (
        b'value="SN-001"'
        in second_response.data
    )

    assert (
        b'value="PLANTA-01"'
        in second_response.data
    )


def test_create_asset_should_reject_invalid_status(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="MOTOR-01",
            name="Motor 10 HP",
            model_number="MTR-10HP",
            manufacturer_code="TEST",
            asset_type_code="MOTOR",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "MOTOR-INVALID-STATUS",
            "name": "Motor estado invalido",
            "asset_model_code": "MOTOR-01",
            "serial_number": "SN-INVALID-01",
            "location_code": "PLANTA-01",
            "status": "INVALID_STATUS",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    assert (
        asset_repository.find_by_code(
            "MOTOR-INVALID-STATUS"
        )
        is None
    )


def test_create_asset_should_reject_invalid_installation_date(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="MOTOR-01",
            name="Motor 10 HP",
            model_number="MTR-10HP",
            manufacturer_code="TEST",
            asset_type_code="MOTOR",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "MOTOR-INVALID-DATE",
            "name": "Motor fecha invalida",
            "asset_model_code": "MOTOR-01",
            "serial_number": "SN-INVALID-DATE",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "30-08-2026",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    assert (
        asset_repository.find_by_code(
            "MOTOR-INVALID-DATE"
        )
        is None
    )

    assert (
        b'value="30-08-2026"'
        in response.data
    )


def test_admin_should_see_new_asset_action(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    assert (
        b"/activos/nuevo"
        in response.data
    )

    assert (
        b"Nuevo activo"
        in response.data
    )


def test_technician_should_not_see_new_asset_action(
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

    assert (
        b"/activos/nuevo"
        not in response.data
    )

    assert (
        b"Nuevo activo"
        not in response.data
    )


def test_assets_index_should_list_persistent_assets(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="MOTOR-INDEX-01",
            name="Motor catalogo",
            model_number="MTR-CAT-01",
            manufacturer_code="TEST",
            asset_type_code="MOTOR",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    asset_repository.save(
        Asset(
            code="MOTOR-PLANTA-01",
            name="Motor bomba 1",
            asset_model_code="MOTOR-INDEX-01",
            serial_number="SN-CATALOG-01",
            location_code="PLANTA-01",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                30,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    assert (
        b"MOTOR-PLANTA-01"
        in response.data
    )

    assert (
        b"Motor bomba 1"
        in response.data
    )

    assert (
        b"PLANTA-01"
        in response.data
    )

    assert (
        b"Operando"
        in response.data
    )


def test_admin_should_open_new_physical_location_form(
    client,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/ubicaciones/nueva"
    )

    assert response.status_code == 200


def test_admin_should_create_physical_location(
    client,
    assets_test_db,
) -> None:

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/ubicaciones/nueva",
        data={
            "code": "PINTURA-MD1",
            "name": "Area de Pintura MD1",
            "area": "MD1",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers[
        "Location"
    ].endswith(
        "/activos/nuevo"
    )

    location = (
        physical_location_repository
        .find_by_code(
            "PINTURA-MD1"
        )
    )

    assert location is not None
    assert location.code == "PINTURA-MD1"
    assert location.name == "Area de Pintura MD1"
    assert location.area == "MD1"
    assert location.is_active is True


def test_admin_should_not_create_duplicate_physical_location(
    client,
    assets_test_db,
) -> None:

    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="PINTURA-MD1",
            name="Area de Pintura MD1",
            area="MD1",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/ubicaciones/nueva",
        data={
            "code": "PINTURA-MD1",
            "name": "Pintura duplicada",
            "area": "MD1",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert (
        "Ya existe una ubicacion con ese codigo."
        in html
    )

    assert 'value="PINTURA-MD1"' in html
    assert 'value="Pintura duplicada"' in html
    assert 'value="MD1"' in html


def test_new_asset_form_should_offer_catalog_creation_links(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        'formaction="/activos/nuevo/borrador/modelo"'
        in html
    )

    assert (
        'formaction="/activos/nuevo/borrador/ubicacion"'
        in html
    )

    assert "Nuevo modelo" in html

    assert (
        "Nueva ubicaci&oacute;n" in html
        or "Nueva ubicaci?n" in html
    )


def test_asset_model_created_from_new_asset_flow_should_return_to_new_asset(
    client,
    asset_models_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/modelos/nuevo",
        data={
            "code": "TAB-TEST-01",
            "name": "Tablero de prueba",
            "model_number": "TEST-01",
            "manufacturer_code": "GENERIC",
            "asset_type_code": "ELECTRICAL-PANEL",
            "description": "Modelo para prueba de flujo.",
            "return_to": "new_asset",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers[
        "Location"
    ].endswith(
        "/activos/nuevo"
    )


def test_asset_model_form_from_new_asset_flow_should_offer_return_to_new_asset(
    client,
    asset_models_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/modelos/nuevo?return_to=new_asset"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        'href="/activos/nuevo"'
        in html
    )


def test_admin_should_create_asset_without_serial_number(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = (
        assets_test_db[
            "asset_repository"
        ]
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-TEST-01",
            name="Panel de prueba",
            model_number="TEST-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="PLANTA-01",
            name="Planta 01",
            area="PRODUCCION",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "PANEL-TEST-01",
            "serial_number": "",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    asset = asset_repository.find_by_code(
        "T-001"
    )

    assert asset is not None
    assert asset.serial_number == ""


def test_new_asset_form_should_treat_serial_number_as_optional(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    serial_start = html.index(
        'id="serial_number"'
    )

    serial_end = html.index(
        ">",
        serial_start,
    )

    serial_input = html[
        serial_start:serial_end
    ]

    assert "required" not in serial_input

    label_start = html.index(
        '<label for="serial_number">'
    )

    label_end = html.index(
        "</label>",
        label_start,
    )

    serial_label = html[
        label_start:label_end
    ]

    assert "(opcional)" in serial_label


def test_new_asset_should_be_available_for_map_placement(
    client,
    assets_test_db,
    monkeypatch,
) -> None:

    import importlib
    from types import SimpleNamespace

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-MAP-TEST-01",
            name="Panel para prueba de mapa",
            model_number="MAP-TEST-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para integracion Assets Maps.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-MAP-TEST-01",
            name="Ubicacion para prueba de mapa",
            area="TEST",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    create_response = client.post(
        "/activos/nuevo",
        data={
            "code": "T-MAP-001",
            "name": "Tablero T-MAP-001",
            "asset_model_code": "PANEL-MAP-TEST-01",
            "serial_number": "",
            "location_code": "LOC-MAP-TEST-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert create_response.status_code == 302

    maps_routes = importlib.import_module(
        "app.maps.routes"
    )

    class FakeFindAllMapLocations:
        def execute(self):
            return SimpleNamespace(
                success=True,
                message="",
                locations=[],
            )

    monkeypatch.setattr(
        maps_routes,
        "find_all_map_locations",
        FakeFindAllMapLocations(),
    )

    available_response = client.get(
        "/maps/api/available-assets"
    )

    assert available_response.status_code == 200

    available_assets = (
        available_response.get_json()
    )

    assert any(
        item["code"] == "T-MAP-001"
        and item["name"] == "Tablero T-MAP-001"
        for item in available_assets
    )


def test_mapped_asset_should_not_be_available_for_map_placement(
    client,
    assets_test_db,
    monkeypatch,
) -> None:

    import importlib
    from types import SimpleNamespace

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-MAP-TEST-02",
            name="Panel mapeado de prueba",
            model_number="MAP-TEST-02",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para prueba de exclusion en Maps.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-MAP-TEST-02",
            name="Ubicacion mapeada de prueba",
            area="TEST",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    create_response = client.post(
        "/activos/nuevo",
        data={
            "code": "T-MAP-002",
            "name": "Tablero T-MAP-002",
            "asset_model_code": "PANEL-MAP-TEST-02",
            "serial_number": "",
            "location_code": "LOC-MAP-TEST-02",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert create_response.status_code == 302

    maps_routes = importlib.import_module(
        "app.maps.routes"
    )

    class FakeFindAllMapLocations:
        def execute(self):
            return SimpleNamespace(
                success=True,
                message="",
                locations=[
                    SimpleNamespace(
                        asset_code="T-MAP-002",
                    )
                ],
            )

    monkeypatch.setattr(
        maps_routes,
        "find_all_map_locations",
        FakeFindAllMapLocations(),
    )

    available_response = client.get(
        "/maps/api/available-assets"
    )

    assert available_response.status_code == 200

    available_assets = (
        available_response.get_json()
    )

    assert all(
        item["code"] != "T-MAP-002"
        for item in available_assets
    )


def test_new_asset_form_should_restore_draft_from_session(
    client,
    assets_test_db,
) -> None:

    draft = {
        "code": "T-001",
        "name": "Tablero Electrico T-001",
        "asset_model_code": "",
        "serial_number": "",
        "location_code": "",
        "status": "OPERATING",
        "installation_date": "2026-08-30",
    }

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"
        session["new_asset_draft"] = draft

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'value="T-001"' in html
    assert (
        'value="Tablero Electrico T-001"'
        in html
    )
    assert 'value="2026-08-30"' in html


def test_new_asset_should_save_draft_before_creating_model(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo/borrador/modelo",
        data={
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "",
            "serial_number": "SERIE-TEST",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        response.headers["Location"]
        .endswith(
            "/activos/modelos/nuevo"
            "?return_to=new_asset"
        )
    )

    with client.session_transaction() as session:
        draft = session.get(
            "new_asset_draft"
        )

    assert draft == {
        "code": "T-001",
        "name": "Tablero Electrico T-001",
        "asset_model_code": "",
        "serial_number": "SERIE-TEST",
        "location_code": "PLANTA-01",
        "status": "OPERATING",
        "installation_date": "2026-08-30",
    }


def test_created_model_should_be_selected_in_new_asset_draft(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"
        session["new_asset_draft"] = {
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "",
            "serial_number": "",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        }

    response = client.post(
        "/activos/modelos/nuevo",
        data={
            "code": "PANEL-TEST-NEW",
            "name": "Panel Test New",
            "model_number": "TEST-NEW",
            "manufacturer_code": "GENERIC",
            "asset_type_code": "ELECTRICAL-PANEL",
            "description": "Modelo creado desde nuevo activo.",
            "return_to": "new_asset",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers[
        "Location"
    ].endswith(
        "/activos/nuevo"
    )

    with client.session_transaction() as session:
        draft = session[
            "new_asset_draft"
        ]

    assert (
        draft["asset_model_code"]
        == "PANEL-TEST-NEW"
    )


def test_new_asset_should_save_draft_before_creating_location(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo/borrador/ubicacion",
        data={
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "PANEL-TEST-01",
            "serial_number": "",
            "location_code": "",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        response.headers["Location"]
        .endswith(
            "/activos/ubicaciones/nueva"
        )
    )

    with client.session_transaction() as session:
        draft = session.get(
            "new_asset_draft"
        )

    assert draft == {
        "code": "T-001",
        "name": "Tablero Electrico T-001",
        "asset_model_code": "PANEL-TEST-01",
        "serial_number": "",
        "location_code": "",
        "status": "OPERATING",
        "installation_date": "2026-08-30",
    }


def test_created_location_should_be_selected_in_new_asset_draft(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"
        session["new_asset_draft"] = {
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "PANEL-TEST-01",
            "serial_number": "",
            "location_code": "",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        }

    response = client.post(
        "/activos/ubicaciones/nueva",
        data={
            "code": "LOC-TEST-NEW",
            "name": "Ubicacion Test New",
            "area": "PLANTA",
            "return_to": "new_asset",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers[
        "Location"
    ].endswith(
        "/activos/nuevo"
    )

    with client.session_transaction() as session:
        draft = session[
            "new_asset_draft"
        ]

    assert (
        draft["location_code"]
        == "LOC-TEST-NEW"
    )


def test_cancel_location_creation_should_restore_new_asset_draft(
    client,
    assets_test_db,
) -> None:

    draft = {
        "code": "T-001",
        "name": "Tablero Electrico T-001",
        "asset_model_code": "PANEL-TEST-01",
        "serial_number": "",
        "location_code": "",
        "status": "OPERATING",
        "installation_date": "2026-08-30",
    }

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"
        session["new_asset_draft"] = draft

    location_response = client.get(
        "/activos/ubicaciones/nueva"
    )

    assert location_response.status_code == 200

    location_html = location_response.get_data(
        as_text=True
    )

    assert (
        'href="/activos/nuevo"'
        in location_html
    )

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'value="T-001"' in html

    assert (
        'value="Tablero Electrico T-001"'
        in html
    )

    assert (
        'value="2026-08-30"'
        in html
    )

    with client.session_transaction() as session:
        assert (
            session["new_asset_draft"]
            == draft
        )


def test_successful_asset_creation_should_clear_new_asset_draft(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository = (
        assets_test_db[
            "asset_model_repository"
        ]
    )

    physical_location_repository = (
        assets_test_db[
            "physical_location_repository"
        ]
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-TEST-01",
            name="Panel de prueba",
            model_number="TEST-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo de prueba.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="PLANTA-01",
            name="Planta 01",
            area="PRODUCCION",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"
        session["new_asset_draft"] = {
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "PANEL-TEST-01",
            "serial_number": "",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        }

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "T-001",
            "name": "Tablero Electrico T-001",
            "asset_model_code": "PANEL-TEST-01",
            "serial_number": "",
            "location_code": "PLANTA-01",
            "status": "OPERATING",
            "installation_date": "2026-08-30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert (
            "new_asset_draft"
            not in session
        )

def test_new_asset_catalog_creation_buttons_should_skip_form_validation(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.data.decode(
        "utf-8"
    )

    model_action = (
        'formaction="/activos/nuevo/'
        'borrador/modelo"'
    )

    location_action = (
        'formaction="/activos/nuevo/'
        'borrador/ubicacion"'
    )

    model_position = html.index(
        model_action
    )

    location_position = html.index(
        location_action
    )

    model_button = html[
        model_position:
        model_position + 250
    ]

    location_button = html[
        location_position:
        location_position + 250
    ]

    assert "formnovalidate" in model_button
    assert "formnovalidate" in location_button

def test_admin_should_open_asset_edit_form(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-01",
            name="Panel Edit Test",
            model_number="EDIT-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para editar activo.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-01",
            name="Ubicacion Edit Test",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-001",
            name="Tablero Edit Test",
            asset_model_code="PANEL-EDIT-01",
            serial_number="SN-EDIT-001",
            location_code="LOC-EDIT-01",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                30,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/T-EDIT-001/editar"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Editar activo" in html
    assert "T-EDIT-001" in html
    assert 'value="Tablero Edit Test"' in html
    assert 'value="SN-EDIT-001"' in html
    assert 'value="2026-08-30"' in html

    model_option_start = html.index(
    'value="PANEL-EDIT-01"'
)

    model_option_end = html.index(
        "</option>",
        model_option_start,
    )

    model_option = html[
        model_option_start:model_option_end
    ]

    assert "selected" in model_option


    location_option_start = html.index(
        'value="LOC-EDIT-01"'
    )

    location_option_end = html.index(
        "</option>",
        location_option_start,
    )

    location_option = html[
        location_option_start:location_option_end
    ]

    assert "selected" in location_option


def test_asset_edit_form_should_return_404_when_asset_does_not_exist(
    client,
    assets_test_db,
) -> None:

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/ASSET-NOT-FOUND/editar"
    )

    assert response.status_code == 404


def test_asset_edit_form_should_not_expose_status_field(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-STATUS",
            name="Panel Edit Status",
            model_number="EDIT-STATUS",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para prueba de status.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-STATUS",
            name="Ubicacion Edit Status",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-STATUS",
            name="Tablero Edit Status",
            asset_model_code=(
                "PANEL-EDIT-STATUS"
            ),
            serial_number="",
            location_code=(
                "LOC-EDIT-STATUS"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                30,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/T-EDIT-STATUS/editar"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'name="status"' not in html
    assert 'id="status"' not in html

def test_admin_should_update_asset_from_edit_form(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-OLD",
            name="Panel Old",
            model_number="OLD",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo original.",
            specifications={},
        )
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-NEW",
            name="Panel New",
            model_number="NEW",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo nuevo.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-OLD",
            name="Ubicacion Old",
            area="TEST",
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-NEW",
            name="Ubicacion New",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-002",
            name="Tablero Original",
            asset_model_code="PANEL-EDIT-OLD",
            serial_number="SN-OLD",
            location_code="LOC-EDIT-OLD",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-EDIT-002/editar",
        data={
            "name": "Tablero Actualizado",
            "asset_model_code": (
                "PANEL-EDIT-NEW"
            ),
            "serial_number": "SN-NEW",
            "location_code": (
                "LOC-EDIT-NEW"
            ),
            "installation_date": (
                "2026-08-31"
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    saved_asset = (
        asset_repository.find_by_code(
            "T-EDIT-002"
        )
    )

    assert saved_asset is not None

    assert saved_asset.code == "T-EDIT-002"

    assert (
        saved_asset.name
        == "Tablero Actualizado"
    )

    assert (
        saved_asset.asset_model_code
        == "PANEL-EDIT-NEW"
    )

    assert (
        saved_asset.serial_number
        == "SN-NEW"
    )

    assert (
        saved_asset.location_code
        == "LOC-EDIT-NEW"
    )

    assert (
        saved_asset.installation_date
        == date(
            2026,
            8,
            31,
        )
    )

    assert (
        saved_asset.status
        == AssetStatus.OPERATING
    )

def test_asset_edit_should_allow_missing_installation_date(
    client,
    assets_test_db,
) -> None:

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-NO-DATE-POST",
            name="Panel Edit No Date Post",
            model_number="EDIT-NO-DATE-POST",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para editar activo "
                "sin fecha."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-NO-DATE-POST",
            name="Ubicacion No Date Post",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-NO-DATE-POST",
            name="Tablero Sin Fecha Original",
            asset_model_code=(
                "PANEL-EDIT-NO-DATE-POST"
            ),
            serial_number="",
            location_code=(
                "LOC-EDIT-NO-DATE-POST"
            ),
            status=AssetStatus.OPERATING,
            installation_date=None,
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-EDIT-NO-DATE-POST/editar",
        data={
            "name": "Tablero Sin Fecha Actualizado",
            "asset_model_code": (
                "PANEL-EDIT-NO-DATE-POST"
            ),
            "serial_number": "",
            "location_code": (
                "LOC-EDIT-NO-DATE-POST"
            ),
            "installation_date": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    saved_asset = (
        asset_repository.find_by_code(
            "T-EDIT-NO-DATE-POST"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.name
        == "Tablero Sin Fecha Actualizado"
    )

    assert (
        saved_asset.installation_date
        is None
    )

    assert (
        saved_asset.status
        == AssetStatus.OPERATING
    )
def test_asset_edit_should_preserve_form_when_date_is_invalid(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-ERROR",
            name="Panel Edit Error",
            model_number="EDIT-ERROR",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para prueba de error.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-ERROR",
            name="Ubicacion Edit Error",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-ERROR",
            name="Nombre Original",
            asset_model_code="PANEL-EDIT-ERROR",
            serial_number="SN-ORIGINAL",
            location_code="LOC-EDIT-ERROR",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-EDIT-ERROR/editar",
        data={
            "name": "Nombre Capturado",
            "asset_model_code": (
                "PANEL-EDIT-ERROR"
            ),
            "serial_number": (
                "SN-CAPTURADO"
            ),
            "location_code": (
                "LOC-EDIT-ERROR"
            ),
            "installation_date": (
                "fecha-invalida"
            ),
        },
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert "Editar activo" in html

    assert (
        "La fecha de instalacion no es valida."
        in html
    )

    assert (
        'value="Nombre Capturado"'
        in html
    )

    assert (
        'value="SN-CAPTURADO"'
        in html
    )

    assert (
        'value="fecha-invalida"'
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-EDIT-ERROR"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.name
        == "Nombre Original"
    )

    assert (
        saved_asset.serial_number
        == "SN-ORIGINAL"
    )

    assert (
        saved_asset.installation_date
        == date(
            2026,
            8,
            1,
        )
    )
def test_asset_edit_should_preserve_form_when_model_does_not_exist(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-MODEL-OLD",
            name="Panel Edit Model Old",
            model_number="EDIT-MODEL-OLD",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo original.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-MODEL",
            name="Ubicacion Edit Model",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-MODEL",
            name="Nombre Original",
            asset_model_code=(
                "PANEL-EDIT-MODEL-OLD"
            ),
            serial_number="SN-ORIGINAL",
            location_code="LOC-EDIT-MODEL",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-EDIT-MODEL/editar",
        data={
            "name": "Nombre Capturado",
            "asset_model_code": (
                "MODEL-NOT-FOUND"
            ),
            "serial_number": (
                "SN-CAPTURADO"
            ),
            "location_code": (
                "LOC-EDIT-MODEL"
            ),
            "installation_date": (
                "2026-08-31"
            ),
        },
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert "Editar activo" in html

    assert (
        "No existe el modelo de activo indicado."
        in html
    )

    assert (
        'value="Nombre Capturado"'
        in html
    )

    assert (
        'value="SN-CAPTURADO"'
        in html
    )

    assert (
        'value="2026-08-31"'
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-EDIT-MODEL"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.name
        == "Nombre Original"
    )

    assert (
        saved_asset.asset_model_code
        == "PANEL-EDIT-MODEL-OLD"
    )

    assert (
        saved_asset.serial_number
        == "SN-ORIGINAL"
    )
def test_asset_edit_should_preserve_form_when_location_does_not_exist(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-EDIT-LOCATION",
            name="Panel Edit Location",
            model_number="EDIT-LOCATION",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para prueba de ubicacion.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-EDIT-LOCATION-OLD",
            name="Ubicacion Original",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-EDIT-LOCATION",
            name="Nombre Original",
            asset_model_code=(
                "PANEL-EDIT-LOCATION"
            ),
            serial_number="SN-ORIGINAL",
            location_code=(
                "LOC-EDIT-LOCATION-OLD"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-EDIT-LOCATION/editar",
        data={
            "name": "Nombre Capturado",
            "asset_model_code": (
                "PANEL-EDIT-LOCATION"
            ),
            "serial_number": (
                "SN-CAPTURADO"
            ),
            "location_code": (
                "LOC-NOT-FOUND"
            ),
            "installation_date": (
                "2026-08-31"
            ),
        },
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert "Editar activo" in html

    assert (
        "No existe la ubicacion fisica indicada."
        in html
        or
        "No existe la ubicación física indicada."
        in html
    )

    assert (
        'value="Nombre Capturado"'
        in html
    )

    assert (
        'value="SN-CAPTURADO"'
        in html
    )

    assert (
        'value="2026-08-31"'
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-EDIT-LOCATION"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.name
        == "Nombre Original"
    )

    assert (
        saved_asset.location_code
        == "LOC-EDIT-LOCATION-OLD"
    )

    assert (
        saved_asset.serial_number
        == "SN-ORIGINAL"
    )
def test_admin_should_deactivate_asset_with_reason(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-DEACTIVATE-01",
            name="Panel Deactivate",
            model_number="DEACTIVATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de desactivacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-DEACTIVATE-01",
            name="Ubicacion Deactivate",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-DEACTIVATE-001",
            name="Tablero Deactivate",
            asset_model_code=(
                "PANEL-DEACTIVATE-01"
            ),
            serial_number="",
            location_code=(
                "LOC-DEACTIVATE-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-DEACTIVATE-001/desactivar",
        data={
            "reason": (
                "Retirado temporalmente de servicio."
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    saved_asset = (
        asset_repository.find_by_code(
            "T-DEACTIVATE-001"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.status
        == AssetStatus.OUT_OF_SERVICE
    )

    assert (
        saved_asset.deactivation_reason
        == "Retirado temporalmente de servicio."
    )
def test_asset_deactivation_should_require_reason(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-DEACTIVATE-02",
            name="Panel Deactivate 02",
            model_number="DEACTIVATE-02",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para validar motivo."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-DEACTIVATE-02",
            name="Ubicacion Deactivate 02",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-DEACTIVATE-002",
            name="Tablero Deactivate 02",
            asset_model_code=(
                "PANEL-DEACTIVATE-02"
            ),
            serial_number="",
            location_code=(
                "LOC-DEACTIVATE-02"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-DEACTIVATE-002/desactivar",
        data={
            "reason": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert (
        "El motivo de desactivacion es obligatorio."
        in html
        or
        "El motivo de desactivación es obligatorio."
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-DEACTIVATE-002"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.status
        == AssetStatus.OPERATING
    )

    assert (
        saved_asset.deactivation_reason
        is None
    )
def test_asset_deactivation_should_reject_already_deactivated_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-DEACTIVATE-03",
            name="Panel Deactivate 03",
            model_number="DEACTIVATE-03",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para validar doble desactivacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-DEACTIVATE-03",
            name="Ubicacion Deactivate 03",
            area="TEST",
        )
    )

    asset = Asset(
        code="T-DEACTIVATE-003",
        name="Tablero Deactivate 03",
        asset_model_code=(
            "PANEL-DEACTIVATE-03"
        ),
        serial_number="",
        location_code=(
            "LOC-DEACTIVATE-03"
        ),
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            8,
            1,
        ),
    )

    asset.deactivate(
        "Motivo original."
    )

    asset_repository.save(
        asset
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-DEACTIVATE-003/desactivar",
        data={
            "reason": (
                "Segundo motivo que no debe aplicarse."
            ),
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert (
        "El activo ya se encuentra desactivado."
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-DEACTIVATE-003"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.status
        == AssetStatus.OUT_OF_SERVICE
    )

    assert (
        saved_asset.deactivation_reason
        == "Motivo original."
    )
def test_admin_should_activate_deactivated_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-ACTIVATE-01",
            name="Panel Activate 01",
            model_number="ACTIVATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de reactivacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-ACTIVATE-01",
            name="Ubicacion Activate 01",
            area="TEST",
        )
    )

    asset = Asset(
        code="T-ACTIVATE-001",
        name="Tablero Activate 01",
        asset_model_code=(
            "PANEL-ACTIVATE-01"
        ),
        serial_number="",
        location_code=(
            "LOC-ACTIVATE-01"
        ),
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            8,
            1,
        ),
    )

    asset.deactivate(
        "Retirado temporalmente de servicio."
    )

    asset_repository.save(
        asset
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-ACTIVATE-001/activar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    saved_asset = (
        asset_repository.find_by_code(
            "T-ACTIVATE-001"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.status
        == AssetStatus.OPERATING
    )

    assert (
        saved_asset.deactivation_reason
        is None
    )
def test_asset_activation_should_reject_already_active_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-ACTIVATE-02",
            name="Panel Activate 02",
            model_number="ACTIVATE-02",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para validar doble activacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-ACTIVATE-02",
            name="Ubicacion Activate 02",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-ACTIVATE-002",
            name="Tablero Activate 02",
            asset_model_code=(
                "PANEL-ACTIVATE-02"
            ),
            serial_number="",
            location_code=(
                "LOC-ACTIVATE-02"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/T-ACTIVATE-002/activar",
        follow_redirects=False,
    )

    assert response.status_code == 400

    html = response.get_data(
        as_text=True
    )

    assert (
        "El activo ya se encuentra activo."
        in html
    )

    saved_asset = (
        asset_repository.find_by_code(
            "T-ACTIVATE-002"
        )
    )

    assert saved_asset is not None

    assert (
        saved_asset.status
        == AssetStatus.OPERATING
    )

    assert (
        saved_asset.deactivation_reason
        is None
    )
def test_assets_index_should_show_edit_action_for_admin(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-EDIT-01",
            name="Panel UI Edit",
            model_number="UI-EDIT-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de accion editar."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-EDIT-01",
            name="Ubicacion UI Edit",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-UI-EDIT-001",
            name="Tablero UI Edit",
            asset_model_code=(
                "PANEL-UI-EDIT-01"
            ),
            serial_number="",
            location_code=(
                "LOC-UI-EDIT-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-EDIT-001" in html

    assert (
        "/activos/T-UI-EDIT-001/editar"
        in html
    )

    assert ">Editar<" in html.replace(
        "\n",
        "",
    ).replace(
        " ",
        "",
    )
def test_assets_index_should_show_deactivate_action_for_operating_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-DEACTIVATE-01",
            name="Panel UI Deactivate",
            model_number="UI-DEACTIVATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de accion desactivar."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-DEACTIVATE-01",
            name="Ubicacion UI Deactivate",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-UI-DEACTIVATE-001",
            name="Tablero UI Deactivate",
            asset_model_code=(
                "PANEL-UI-DEACTIVATE-01"
            ),
            serial_number="",
            location_code=(
                "LOC-UI-DEACTIVATE-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-DEACTIVATE-001" in html

    assert (
        "/activos/T-UI-DEACTIVATE-001/desactivar"
        in html
    )

    assert ">Desactivar<" in html.replace(
        "\n",
        "",
    ).replace(
        " ",
        "",
    )
def test_assets_index_should_show_activate_action_for_out_of_service_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-ACTIVATE-01",
            name="Panel UI Activate",
            model_number="UI-ACTIVATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de accion reactivar."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-ACTIVATE-01",
            name="Ubicacion UI Activate",
            area="TEST",
        )
    )

    asset = Asset(
        code="T-UI-ACTIVATE-001",
        name="Tablero UI Activate",
        asset_model_code=(
            "PANEL-UI-ACTIVATE-01"
        ),
        serial_number="",
        location_code=(
            "LOC-UI-ACTIVATE-01"
        ),
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            8,
            1,
        ),
    )

    asset.deactivate(
        "Fuera de servicio para prueba."
    )

    asset_repository.save(
        asset
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-ACTIVATE-001" in html

    assert (
        "/activos/T-UI-ACTIVATE-001/activar"
        in html
    )

    assert ">Reactivar<" in html.replace(
        "\n",
        "",
    ).replace(
        " ",
        "",
    )
def test_assets_index_should_hide_management_actions_without_permission(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-PERMISSION-01",
            name="Panel UI Permission",
            model_number="UI-PERMISSION-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de permisos UI."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-PERMISSION-01",
            name="Ubicacion UI Permission",
            area="TEST",
        )
    )

    operating_asset = Asset(
        code="T-UI-PERMISSION-OPERATING",
        name="Activo Operando Permission",
        asset_model_code=(
            "PANEL-UI-PERMISSION-01"
        ),
        serial_number="",
        location_code=(
            "LOC-UI-PERMISSION-01"
        ),
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            8,
            1,
        ),
    )

    out_of_service_asset = Asset(
        code="T-UI-PERMISSION-OOS",
        name="Activo Fuera Servicio Permission",
        asset_model_code=(
            "PANEL-UI-PERMISSION-01"
        ),
        serial_number="",
        location_code=(
            "LOC-UI-PERMISSION-01"
        ),
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            8,
            1,
        ),
    )

    out_of_service_asset.deactivate(
        "Fuera de servicio para prueba."
    )

    asset_repository.save(
        operating_asset
    )

    asset_repository.save(
        out_of_service_asset
    )

    with client.session_transaction() as session:
        session["username"] = "technician"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-PERMISSION-OPERATING" in html
    assert "T-UI-PERMISSION-OOS" in html

    assert (
        "/activos/T-UI-PERMISSION-OPERATING/editar"
        not in html
    )

    assert (
        "/activos/T-UI-PERMISSION-OPERATING/desactivar"
        not in html
    )

    assert (
        "/activos/T-UI-PERMISSION-OOS/editar"
        not in html
    )

    assert (
        "/activos/T-UI-PERMISSION-OOS/activar"
        not in html
    )
def test_assets_index_should_request_reason_before_deactivating_asset(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-DEACTIVATE-01",
            name="Panel UI Deactivate",
            model_number="UI-DEACTIVATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de motivo "
                "de desactivacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-DEACTIVATE-01",
            name="Ubicacion UI Deactivate",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-UI-DEACTIVATE-001",
            name="Tablero UI Deactivate",
            asset_model_code=(
                "PANEL-UI-DEACTIVATE-01"
            ),
            serial_number="",
            location_code=(
                "LOC-UI-DEACTIVATE-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-DEACTIVATE-001" in html

    assert (
        "/activos/T-UI-DEACTIVATE-001/desactivar"
        in html
    )

    assert 'name="reason"' in html

    assert 'required' in html

    assert "Motivo de desactivaci" in html

    assert (
        "Confirmar desactivaci"
        in html
    )
def test_assets_index_should_present_unavailable_asset_data_cleanly(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-NODATA-01",
            name="Panel UI No Data",
            model_number="UI-NODATA-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de datos "
                "no disponibles."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-NODATA-01",
            name="Ubicacion UI No Data",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-UI-NODATA-001",
            name="Tablero UI No Data",
            asset_model_code=(
                "PANEL-UI-NODATA-01"
            ),
            serial_number="",
            location_code=(
                "LOC-UI-NODATA-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-NODATA-001" in html

    assert "None%" not in html
    assert ">None<" not in html

    assert "<progress" not in html
def test_assets_index_should_present_available_health_value(
    client,
    assets_test_db,
    monkeypatch,
) -> None:

    from app.assets.presenters.asset_presenter import (
        AssetPresenter,
    )

    original_present = AssetPresenter.present

    def present_with_health(
        asset,
        physical_location=None,
    ):
        view = original_present(
            asset,
            physical_location=physical_location,
        )

        if view.codigo == "T-UI-HEALTH-001":
            view.salud = 84

        return view

    monkeypatch.setattr(
        AssetPresenter,
        "present",
        staticmethod(present_with_health),
    )

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-UI-HEALTH-01",
            name="Panel UI Health",
            model_number="UI-HEALTH-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de salud disponible."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-UI-HEALTH-01",
            name="Ubicacion UI Health",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-UI-HEALTH-001",
            name="Tablero UI Health",
            asset_model_code=(
                "PANEL-UI-HEALTH-01"
            ),
            serial_number="",
            location_code=(
                "LOC-UI-HEALTH-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-UI-HEALTH-001" in html
    assert "84%" in html
    assert "<progress" in html
    assert 'value="84"' in html
def test_assets_index_should_present_physical_location_name_and_area(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-LOCATION-UI-01",
            name="Panel Location UI",
            model_number="LOCATION-UI-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de ubicacion."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-AREA-001",
            name="Subestacion Norte",
            area="Servicios",
        )
    )

    asset_repository.save(
        Asset(
            code="T-LOCATION-UI-001",
            name="Tablero Location UI",
            asset_model_code=(
                "PANEL-LOCATION-UI-01"
            ),
            serial_number="",
            location_code="LOC-AREA-001",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-LOCATION-UI-001" in html
    assert "Servicios" in html
    assert "Subestacion Norte" in html
def test_asset_detail_should_present_physical_location_name_and_area(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-LIFE-LOCATION-01",
            name="Panel Life Location",
            model_number="LIFE-LOCATION-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de ubicacion "
                "en hoja de vida."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-LIFE-SHEET-001",
            name="Subestacion Principal",
            area="Servicios",
        )
    )

    asset_repository.save(
        Asset(
            code="T-LIFE-LOCATION-001",
            name="Tablero Life Location",
            asset_model_code=(
                "PANEL-LIFE-LOCATION-01"
            ),
            serial_number="",
            location_code="LOC-LIFE-SHEET-001",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activo/T-LIFE-LOCATION-001"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-LIFE-LOCATION-001" in html
    assert "Subestacion Principal" in html
    assert "Servicios" in html
def test_asset_api_should_present_physical_location_name_and_area(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-API-LOCATION-01",
            name="Panel API Location",
            model_number="API-LOCATION-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de ubicacion "
                "en API de activo."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-API-001",
            name="Subestacion API",
            area="Servicios",
        )
    )

    asset_repository.save(
        Asset(
            code="T-API-LOCATION-001",
            name="Tablero API Location",
            asset_model_code=(
                "PANEL-API-LOCATION-01"
            ),
            serial_number="",
            location_code="LOC-API-001",
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/assets/api/T-API-LOCATION-001"
    )

    assert response.status_code == 200

    payload = response.get_json()

    assert payload["codigo"] == "T-API-LOCATION-001"
    assert payload["ubicacion"] == "Subestacion API"
    assert payload["area"] == "Servicios"

def test_asset_detail_should_not_invent_health_when_not_evaluated(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-LIFE-NO-HEALTH-01",
            name="Panel Life No Health",
            model_number="LIFE-NO-HEALTH-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba de salud "
                "no evaluada."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-LIFE-NO-HEALTH-01",
            name="Ubicacion No Health",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-LIFE-NO-HEALTH-001",
            name="Tablero Life No Health",
            asset_model_code=(
                "PANEL-LIFE-NO-HEALTH-01"
            ),
            serial_number="",
            location_code=(
                "LOC-LIFE-NO-HEALTH-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activo/T-LIFE-NO-HEALTH-001"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "T-LIFE-NO-HEALTH-001" in html
    assert "Sin evaluar" in html
    assert "100%" not in html

def test_asset_api_should_return_null_health_when_not_evaluated(
    client,
    assets_test_db,
) -> None:

    from datetime import date

    from app.domains.assets.entities.asset import (
        Asset,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.assets.value_objects.asset_status import (
        AssetStatus,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_repository = assets_test_db[
        "asset_repository"
    ]

    asset_model_repository = assets_test_db[
        "asset_model_repository"
    ]

    physical_location_repository = assets_test_db[
        "physical_location_repository"
    ]

    asset_model_repository.save(
        AssetModel(
            code="PANEL-API-NO-HEALTH-01",
            name="Panel API No Health",
            model_number="API-NO-HEALTH-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description=(
                "Modelo para prueba API de "
                "salud no evaluada."
            ),
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-API-NO-HEALTH-01",
            name="Ubicacion API No Health",
            area="TEST",
        )
    )

    asset_repository.save(
        Asset(
            code="T-API-NO-HEALTH-001",
            name="Tablero API No Health",
            asset_model_code=(
                "PANEL-API-NO-HEALTH-01"
            ),
            serial_number="",
            location_code=(
                "LOC-API-NO-HEALTH-01"
            ),
            status=AssetStatus.OPERATING,
            installation_date=date(
                2026,
                8,
                1,
            ),
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/assets/api/T-API-NO-HEALTH-001"
    )

    assert response.status_code == 200

    payload = response.get_json()

    assert payload["codigo"] == "T-API-NO-HEALTH-001"
    assert payload["salud"] is None
def test_new_asset_should_allow_empty_installation_date(
    client,
    assets_test_db,
) -> None:
    from app.domains.assets.bootstrap.assets_container import (
        asset_model_repository,
        repository as asset_repository,
    )
    from app.domains.assets.entities.asset_model import (
        AssetModel,
    )
    from app.domains.locations.bootstrap.locations_container import (
        repository as physical_location_repository,
    )
    from app.domains.locations.entities.physical_location import (
        PhysicalLocation,
    )

    asset_model_repository.save(
        AssetModel(
            code="PANEL-NO-DATE-01",
            name="Panel No Date",
            model_number="PANEL-NO-DATE-01",
            manufacturer_code="GENERIC",
            asset_type_code="ELECTRICAL-PANEL",
            description="Modelo para prueba sin fecha.",
            specifications={},
        )
    )

    physical_location_repository.save(
        PhysicalLocation(
            code="LOC-NO-DATE-01",
            name="Ubicacion No Date",
            area="PRUEBAS",
        )
    )

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.post(
        "/activos/nuevo",
        data={
            "code": "T-NO-DATE-001",
            "name": "Tablero Sin Fecha",
            "asset_model_code": "PANEL-NO-DATE-01",
            "serial_number": "",
            "location_code": "LOC-NO-DATE-01",
            "status": "OPERATING",
            "installation_date": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    saved_asset = asset_repository.find_by_code(
        "T-NO-DATE-001"
    )

    assert saved_asset is not None
    assert saved_asset.installation_date is None
def test_new_asset_installation_date_should_be_optional_in_form(
    client,
    assets_test_db,
) -> None:
    with client.session_transaction() as session:
        session["username"] = "admin"
        session["person_code"] = "ADMIN-001"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/activos/nuevo"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        "Fecha de instalación (opcional)"
        in html
    )

    installation_date_position = html.index(
        'name="installation_date"'
    )

    installation_date_input = html[
        installation_date_position:
        installation_date_position + 250
    ]

    assert "required" not in installation_date_input
