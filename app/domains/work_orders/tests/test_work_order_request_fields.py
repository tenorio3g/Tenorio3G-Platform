from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)


def build_work_order(
    *,
    asset_code="ASSET-001",
    requester_person_code="REQ-001",
    supervisor_person_code="SUP-001",
    requester_name=None,
    requester_phone=None,
    requester_area=None,
    location_description=None,
):

    return WorkOrder(
        code="WO-001",
        title="Instalar contacto 110 V",
        description=(
            "Instalar contacto y salida "
            "de aire comprimido."
        ),
        work_type="CORRECTIVE",
        priority="MEDIUM",
        asset_code=asset_code,
        requester_person_code=(
            requester_person_code
        ),
        supervisor_person_code=(
            supervisor_person_code
        ),
        created_at=datetime(
            2026,
            8,
            22,
            8,
            0,
        ),
        requester_name=requester_name,
        requester_phone=requester_phone,
        requester_area=requester_area,
        location_description=(
            location_description
        ),
    )


def test_should_allow_work_order_without_asset():

    work_order = build_work_order(
        asset_code=None,
    )

    assert work_order.asset_code is None


def test_should_allow_work_order_without_supervisor():

    work_order = build_work_order(
        supervisor_person_code=None,
    )

    assert (
        work_order.supervisor_person_code
        is None
    )


def test_should_allow_registered_requester():

    work_order = build_work_order(
        requester_person_code="REQ-001",
        requester_name=None,
        requester_phone=None,
    )

    assert (
        work_order.requester_person_code
        == "REQ-001"
    )


def test_should_allow_manual_requester():

    work_order = build_work_order(
        requester_person_code=None,
        requester_name="Juan Perez",
        requester_phone="1234",
        requester_area="Produccion MD2",
    )

    assert (
        work_order.requester_person_code
        is None
    )

    assert (
        work_order.requester_name
        == "Juan Perez"
    )

    assert (
        work_order.requester_phone
        == "1234"
    )

    assert (
        work_order.requester_area
        == "Produccion MD2"
    )


def test_should_require_manual_requester_name():

    with pytest.raises(
        ValueError,
        match="requester name is required",
    ):

        build_work_order(
            requester_person_code=None,
            requester_name="",
            requester_phone="1234",
        )


def test_should_require_manual_requester_phone():

    with pytest.raises(
        ValueError,
        match="requester phone is required",
    ):

        build_work_order(
            requester_person_code=None,
            requester_name="Juan Perez",
            requester_phone="",
        )


def test_should_allow_location_without_asset():

    work_order = build_work_order(
        asset_code=None,
        location_description=(
            "Estacionamiento norte"
        ),
    )

    assert (
        work_order.location_description
        == "Estacionamiento norte"
    )


def test_should_normalize_optional_codes():

    work_order = build_work_order(
        asset_code=" asset-001 ",
        requester_person_code=" req-001 ",
        supervisor_person_code=" sup-001 ",
    )

    assert (
        work_order.asset_code
        == "ASSET-001"
    )

    assert (
        work_order.requester_person_code
        == "REQ-001"
    )

    assert (
        work_order.supervisor_person_code
        == "SUP-001"
    )
