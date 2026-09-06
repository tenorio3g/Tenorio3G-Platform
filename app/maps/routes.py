from __future__ import annotations

from flask import jsonify, render_template, request

from . import maps

from app.domains.assets.bootstrap import (
    find_all_assets,
)

from app.domains.assets.use_cases.find_all_assets.query import (
    FindAllAssetsQuery,
)

from app.maps.bootstrap import (
    find_all_map_locations,
    move_asset_on_map,
    place_asset_on_map,
)

from app.maps.presenters import (
    MapLocationPresenter,
)

from app.maps.use_cases.move_asset_on_map.command import (
    MoveAssetOnMapCommand,
)

from app.maps.use_cases.place_asset_on_map.command import (
    PlaceAssetOnMapCommand,
)


@maps.route("")
@maps.route("/")
def index():
    """
    Pantalla principal del modulo Maps.
    """

    return render_template(
        "pages/map.html",
    )


@maps.get("/api/locations")
def api_locations():
    """
    Devuelve las ubicaciones registradas en formato JSON.
    """

    result = find_all_map_locations.execute()

    payload = MapLocationPresenter.present_many(
        result.locations,
    )

    return jsonify(payload)


@maps.get("/api/available-assets")
def api_available_assets():
    """
    Devuelve los activos que aun no tienen posicion
    registrada en el mapa.
    """

    assets_result = find_all_assets.execute(
        FindAllAssetsQuery()
    )

    locations_result = (
        find_all_map_locations.execute()
    )

    placed_asset_codes = {
        location.asset_code
        for location
        in locations_result.locations
    }

    payload = [
        {
            "code": asset.code,
            "name": asset.name,
        }
        for asset in assets_result.assets
        if asset.code not in placed_asset_codes
    ]

    return jsonify(payload)


@maps.post("/api/locations")
def api_place_asset():
    """
    Registra la posicion de un activo existente
    dentro del mapa.
    """

    data = request.get_json(
        silent=True,
    )

    if not isinstance(data, dict):
        return (
            jsonify(
                {
                    "success": False,
                    "message": (
                        "La solicitud debe contener "
                        "un objeto JSON valido."
                    ),
                }
            ),
            400,
        )

    try:
        command = PlaceAssetOnMapCommand(
            asset_code=data["asset_code"],
            category=data["category"],
            x=float(data["x"]),
            y=float(data["y"]),
        )
    except (
        KeyError,
        TypeError,
        ValueError,
    ):
        return (
            jsonify(
                {
                    "success": False,
                    "message": (
                        "Los datos para colocar el activo "
                        "son invalidos."
                    ),
                }
            ),
            400,
        )

    result = place_asset_on_map.execute(
        command
    )

    if not result.success:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.message,
                }
            ),
            400,
        )

    location_payload = (
        MapLocationPresenter.present_many(
            [result.location]
        )[0]
    )

    return (
        jsonify(
            {
                "success": True,
                "message": result.message,
                "location": location_payload,
            }
        ),
        201,
    )


@maps.patch("/api/locations/<asset_code>")
def api_move_asset(
    asset_code: str,
):
    """
    Reubica un activo que ya tiene una posicion
    registrada dentro del mapa.
    """

    data = request.get_json(
        silent=True,
    )

    if not isinstance(data, dict):
        return (
            jsonify(
                {
                    "success": False,
                    "message": (
                        "La solicitud debe contener "
                        "un objeto JSON valido."
                    ),
                }
            ),
            400,
        )

    try:
        command = MoveAssetOnMapCommand(
            asset_code=asset_code,
            x=float(data["x"]),
            y=float(data["y"]),
        )
    except (
        KeyError,
        TypeError,
        ValueError,
    ):
        return (
            jsonify(
                {
                    "success": False,
                    "message": (
                        "Los datos para reubicar el activo "
                        "son invalidos."
                    ),
                }
            ),
            400,
        )

    result = move_asset_on_map.execute(
        command
    )

    if not result.success:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.message,
                }
            ),
            400,
        )

    location_payload = (
        MapLocationPresenter.present_many(
            [result.location]
        )[0]
    )

    return jsonify(
        {
            "success": True,
            "message": result.message,
            "location": location_payload,
        }
    )
