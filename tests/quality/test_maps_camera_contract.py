from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MAP_JS_PATH = (
    PROJECT_ROOT
    / "app"
    / "maps"
    / "static"
    / "js"
    / "map.js"
)

MAP_TEMPLATE_PATH = (
    PROJECT_ROOT
    / "app"
    / "maps"
    / "templates"
    / "pages"
    / "map.html"
)


def test_map_should_use_centralized_camera_state():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "const camera =" in source
    assert "function aplicarCamara()" in source

    assert "camera.scale" in source
    assert "camera.x" in source
    assert "camera.y" in source


def test_map_should_define_zoom_limits():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "MIN_MAP_SCALE" in source
    assert "MAX_MAP_SCALE" in source


def test_map_should_offer_reset_view_control():
    source = MAP_TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert 'id="restablecerVistaMapa"' in source
    assert 'id="nivelZoomMapa"' in source

def test_map_should_support_pointer_pan_navigation():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "PAN_DRAG_THRESHOLD" in source
    assert "function iniciarPanMapa(" in source
    assert "function moverPanMapa(" in source
    assert "function finalizarPanMapa(" in source

    assert '"pointerdown"' in source
    assert '"pointermove"' in source
    assert '"pointerup"' in source


def test_map_should_support_wheel_zoom():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function manejarZoomRueda(" in source
    assert '"wheel"' in source
    assert "event.preventDefault()" in source


def test_map_pan_should_update_camera_not_asset_coordinates():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "camera.x" in source
    assert "camera.y" in source

    pan_start = source.index(
        "function moverPanMapa("
    )

    pan_end = source.index(
        "function finalizarPanMapa(",
        pan_start
    )

    pan_source = source[
        pan_start:pan_end
    ]

    assert "camera.x" in pan_source
    assert "camera.y" in pan_source
    assert "posicionPendiente" not in pan_source
