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