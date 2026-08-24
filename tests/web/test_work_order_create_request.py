import pytest


def test_new_work_order_form_should_allow_optional_asset(
    authenticated_client,
):
    response = authenticated_client.get(
        "/ordenes/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'name="codigo_activo"' in html

    # El activo ya no debe ser obligatorio.
    asset_position = html.find(
        'name="codigo_activo"'
    )

    asset_fragment = html[
        max(0, asset_position - 250):
        asset_position + 250
    ]

    assert "required" not in asset_fragment


def test_new_work_order_form_should_allow_optional_supervisor(
    authenticated_client,
):
    response = authenticated_client.get(
        "/ordenes/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'name="numero_supervisor"' in html

    supervisor_position = html.find(
        'name="numero_supervisor"'
    )

    supervisor_fragment = html[
        max(0, supervisor_position - 250):
        supervisor_position + 250
    ]

    assert "required" not in supervisor_fragment


def test_new_work_order_form_should_have_manual_requester_fields(
    authenticated_client,
):
    response = authenticated_client.get(
        "/ordenes/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'name="nombre_solicitante"' in html
    assert 'name="telefono_solicitante"' in html
    assert 'name="area_solicitante"' in html


def test_new_work_order_form_should_have_location_description(
    authenticated_client,
):
    response = authenticated_client.get(
        "/ordenes/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'name="ubicacion"' in html


def test_should_create_work_order_with_manual_requester_from_web(
    authenticated_client,
    work_orders_test_db,
):
    response = authenticated_client.post(
        "/ordenes/nueva",
        data={
            "numero": "WO-WEB-MANUAL-001",
            "titulo": "Instalar contacto 110 V",
            "descripcion": (
                "Instalar contacto eléctrico "
                "y manguera de aire comprimido."
            ),
            "tipo": "Proyecto",
            "prioridad": "Media",
            "codigo_activo": "",
            "numero_solicitante": "",
            "nombre_solicitante": "Juan Perez",
            "telefono_solicitante": "8991234567",
            "area_solicitante": "Produccion",
            "numero_supervisor": "",
            "ubicacion": "Linea 4, estacion 12",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/ordenes/WO-WEB-MANUAL-001"
        in response.headers["Location"]
    )

