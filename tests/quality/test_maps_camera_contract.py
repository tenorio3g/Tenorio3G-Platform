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

def test_map_search_should_focus_asset_with_camera():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function enfocarActivoMapa(" in source
    assert "camera.x" in source
    assert "camera.y" in source
    assert "aplicarCamara()" in source


def test_map_focus_should_use_viewport_center():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function enfocarActivoMapa("
    )

    end = source.index(
        "function buscarEquipo(",
        start
    )

    focus_source = source[start:end]

    assert "mapViewport" in focus_source
    assert "getBoundingClientRect()" in focus_source
    assert "camera.x" in focus_source
    assert "camera.y" in focus_source


def test_map_search_should_call_asset_focus():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function buscarEquipo("
    )

    end = source.index(
        "function zoomMapa(",
        start
    )

    search_source = source[start:end]

    assert "enfocarActivoMapa(" in search_source

def test_map_search_should_support_short_asset_identifier():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function obtenerIdentificadorCorto(" in source
    assert '.split("-")' in source
    assert ".pop()" in source


def test_map_search_should_match_short_asset_identifier():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function buscarEquipo("
    )

    end = source.index(
        "function zoomMapa(",
        start
    )

    search_source = source[start:end]

    assert "obtenerIdentificadorCorto(" in search_source


def test_map_search_should_run_when_pressing_enter():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert '"keydown"' in source
    assert 'event.key === "Enter"' in source
    assert "buscarEquipo()" in source

def test_map_search_should_collect_all_matches_before_focusing():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "const coincidencias = []" in source
    assert "coincidencias.push(" in source


def test_map_search_should_distinguish_zero_one_and_multiple_matches():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function buscarEquipo("
    )

    end = source.index(
        "function zoomMapa(",
        start
    )

    search_source = source[start:end]

    assert "coincidencias.length === 0" in search_source
    assert "coincidencias.length === 1" in search_source
    assert "coincidencias.length > 1" in search_source


def test_map_should_render_multiple_search_results():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function mostrarResultadosBusqueda(" in source
    assert "function limpiarResultadosBusqueda(" in source
    assert "obtenerIdentificadorCorto(" in source


def test_map_template_should_include_search_results_container():
    source = MAP_TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert 'id="resultadosBusquedaMapa"' in source
