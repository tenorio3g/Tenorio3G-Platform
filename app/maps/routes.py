from flask import jsonify, render_template

from . import maps

from app.maps.bootstrap import find_all_map_locations
from app.maps.presenters import MapLocationPresenter


@maps.route("")
@maps.route("/")
def index():
    """
    Pantalla principal del módulo Maps.
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