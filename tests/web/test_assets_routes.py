from io import BytesIO


def test_assets_index_should_respond(
    client,
) -> None:

    response = client.get(
        "/activos"
    )

    assert response.status_code == 200


def test_create_document_form_should_respond(
    client,
) -> None:

    response = client.get(
        "/activo/S2-480-ES09-T269/documentos/nuevo"
    )

    assert response.status_code == 200

    assert b"Registrar documento" in response.data


def test_create_document_should_persist_and_redirect(
    client,
    documents_test_db,
) -> None:

    response = client.post(
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
    client,
    documents_test_db,
) -> None:

    # Primero creamos el documento de prueba.
    client.post(
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
    response = client.post(
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
    client,
    documents_test_db,
) -> None:

    # Creamos primero el documento de prueba.
    client.post(
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
    response = client.post(
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
    client,
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

    response = client.post(
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
    client,
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
    response = client.post(
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
    response = client.get(
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
    client,
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

    response = client.post(
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

    response = client.post(
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
    client,
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

    response = client.post(
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