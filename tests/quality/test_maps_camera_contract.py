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


POPUP_JS_PATH = (
    PROJECT_ROOT
    / "app"
    / "maps"
    / "static"
    / "js"
    / "popup.js"
)


MAP_HTML_PATH = (
    PROJECT_ROOT
    / "app"
    / "maps"
    / "templates"
    / "pages"
    / "map.html"
)

MAP_CSS_PATH = (
    PROJECT_ROOT
    / "app"
    / "maps"
    / "static"
    / "css"
    / "maps.css"
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

def test_map_should_define_controlled_relocation_state():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "const modoUbicacion = {" in source
    assert 'tipo: "place"' in source
    assert "assetCode: null" in source
    assert "originalX: null" in source
    assert "originalY: null" in source


def test_map_should_support_starting_asset_relocation():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function iniciarReubicacionActivo(" in source
    assert "modoUbicacion.tipo" in source
    assert '"move"' in source
    assert "modoUbicacion.assetCode =" in source


def test_map_should_preserve_original_coordinates_when_relocating():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function iniciarReubicacionActivo("
    )

    end = source.index(
        "function seleccionarPosicion(",
        start,
    )

    relocation_source = source[
        start:end
    ]

    assert "modoUbicacion.originalX =" in relocation_source
    assert "modoUbicacion.originalY =" in relocation_source

def test_map_position_selection_should_support_move_mode():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function seleccionarPosicion("
    )

    end = source.index(
        "function mostrarMarcadorProvisional(",
        start,
    )

    selection_source = source[
        start:end
    ]

    assert 'modoUbicacion.tipo === "move"' in selection_source
    assert "modoUbicacion.assetCode" in selection_source


def test_map_move_mode_should_not_depend_on_available_asset_selector():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function obtenerActivoParaPosicion()" in source
    assert 'modoUbicacion.tipo === "move"' in source
    assert "return modoUbicacion.assetCode;" in source


def test_map_relocation_should_keep_new_coordinates_pending_until_save():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function seleccionarPosicion("
    )

    end = source.index(
        "function mostrarMarcadorProvisional(",
        start,
    )

    selection_source = source[
        start:end
    ]

    assert "posicionPendiente =" in selection_source
    assert "mostrarMarcadorProvisional(" in selection_source

def test_map_should_save_new_location_with_post():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "async function guardarPosicionSeleccionada("
    )

    end = source.index(
        "function actualizarEstadoPosicion(",
        start,
    )

    save_source = source[start:end]

    assert 'method: "POST"' in save_source


def test_map_should_save_relocation_with_patch():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert 'modoUbicacion.tipo === "move"' in source
    assert 'method: "PATCH"' in source
    assert "modoUbicacion.assetCode" in source


def test_map_should_build_relocation_url_from_asset_code():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "encodeURIComponent(" in source
    assert "modoUbicacion.assetCode" in source

def test_map_marker_should_expose_controlled_relocation_action():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function renderPuntos("
    )

    end = source.index(
        "function limitarEscalaMapa(",
        start,
    )

    render_source = source[start:end]

    assert "abrirPopup(" in render_source


def test_starting_relocation_should_inform_user():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function iniciarReubicacionActivo("
    )

    end = source.index(
        "function obtenerActivoParaPosicion()",
        start,
    )

    relocation_source = source[start:end]

    assert "actualizarEstadoPosicion(" in relocation_source
    assert "Selecciona la nueva posicion" in relocation_source


def test_starting_relocation_should_clear_previous_pending_position():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function iniciarReubicacionActivo("
    )

    end = source.index(
        "function obtenerActivoParaPosicion()",
        start,
    )

    relocation_source = source[start:end]

    assert "limpiarPosicionPendiente()" in relocation_source


def test_popup_should_remember_marker_that_opened_it():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "let marcadorPopupActual = null;" in source
    assert "marcadorPopupActual = elemento;" in source


def test_popup_should_offer_relocation_action():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "Reubicar" in source
    assert "reubicarActivoDesdePopup()" in source


def test_popup_relocation_should_delegate_to_map():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function reubicarActivoDesdePopup()" in source
    assert "iniciarReubicacionActivo(" in source
    assert "marcadorPopupActual" in source

def test_map_should_define_location_mode_reset():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function restablecerModoUbicacion()" in source
    assert "modoUbicacion.tipo" in source
    assert '"place"' in source
    assert "modoUbicacion.assetCode" in source
    assert "modoUbicacion.originalX" in source
    assert "modoUbicacion.originalY" in source


def test_cancel_position_should_reset_location_mode():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "if (cancelarPosicion) {"
    )

    end = source.index(
        "if (restablecerVistaMapa)",
        start,
    )

    cancel_source = source[start:end]

    assert "limpiarPosicionPendiente()" in cancel_source
    assert "restablecerModoUbicacion()" in cancel_source


def test_successful_relocation_should_use_location_mode_reset():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "async function guardarPosicionSeleccionada("
    )

    end = source.index(
        "function actualizarEstadoPosicion(",
        start,
    )

    save_source = source[start:end]

    assert "restablecerModoUbicacion()" in save_source


def test_map_should_define_relocation_overlay():
    html = MAP_HTML_PATH.read_text(
        encoding="utf-8"
    )

    assert 'id="mapRelocationOverlay"' in html
    assert 'class="map-relocation-overlay"' in html
    assert 'id="mapRelocationStatus"' in html
    assert 'id="guardarReubicacion"' in html
    assert 'id="cancelarReubicacion"' in html


def test_relocation_overlay_should_be_anchored_to_viewport():
    css = MAP_CSS_PATH.read_text(
        encoding="utf-8"
    )

    assert ".map-relocation-overlay {" in css
    assert "position: absolute;" in css
    assert "z-index:" in css


def test_map_should_control_relocation_overlay():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert 'document.getElementById("mapRelocationOverlay")' in source
    assert 'document.getElementById("mapRelocationStatus")' in source
    assert 'document.getElementById("guardarReubicacion")' in source
    assert 'document.getElementById("cancelarReubicacion")' in source


def test_starting_relocation_should_show_overlay():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function iniciarReubicacionActivo("
    )

    end = source.index(
        "function restablecerModoUbicacion()",
        start,
    )

    relocation_source = source[start:end]

    assert "mostrarControlesReubicacion(" in relocation_source


def test_relocation_overlay_should_update_pending_coordinates():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function seleccionarPosicion("
    )

    end = source.index(
        "function mostrarMarcadorProvisional(",
        start,
    )

    selection_source = source[start:end]

    assert "actualizarControlesReubicacion(" in selection_source


def test_relocation_cancel_should_be_available_before_new_position():
    source = MAP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "cancelarReubicacion.disabled" not in source


def test_relocation_save_should_start_disabled():
    html = MAP_HTML_PATH.read_text(
        encoding="utf-8"
    )

    start = html.index(
        'id="guardarReubicacion"'
    )

    button_source = html[
        max(0, start - 120):
        start + 200
    ]

    assert "disabled" in button_source


def test_popup_should_define_short_asset_identifier():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "function obtenerCodigoCortoActivo(" in source
    assert 'split("-")' in source


def test_popup_should_prioritize_operational_information():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function construirPopupActivo("
    )

    end = source.index(
        "async function abrirPopup(",
        start,
    )

    popup_source = source[start:end]

    assert "obtenerCodigoCortoActivo(" in popup_source
    assert "Ubicación" in popup_source
    assert "Área" in popup_source
    assert "Condición" in popup_source
    assert "Abrir Hoja de Vida" in popup_source
    assert "Reubicar" in popup_source


def test_popup_should_not_show_detailed_technical_information():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function construirPopupActivo("
    )

    end = source.index(
        "async function abrirPopup(",
        start,
    )

    popup_source = source[start:end]

    assert "Modelo" not in popup_source
    assert "?ltimo mantenimiento" not in popup_source
    assert "Pr?ximo mantenimiento" not in popup_source
    assert "Salud del activo" not in popup_source
    assert "Activo industrial" not in popup_source


def test_popup_should_treat_missing_health_as_not_evaluated():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function construirPopupActivo("
    )

    end = source.index(
        "async function abrirPopup(",
        start,
    )

    popup_source = source[start:end]

    assert "activo.salud !== null" in popup_source
    assert "activo.salud !== undefined" in popup_source
    assert 'activo.salud !== ""' in popup_source
    assert '"Sin evaluar"' in popup_source


def test_popup_should_keep_full_asset_code():
    source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    start = source.index(
        "function construirPopupActivo("
    )

    end = source.index(
        "async function abrirPopup(",
        start,
    )

    popup_source = source[start:end]

    assert "activo.codigo" in popup_source
    assert "asset-popup__code" in popup_source


def test_map_should_load_popup_stylesheet():
    source = MAP_HTML_PATH.read_text(
        encoding="utf-8"
    )

    assert "css/popup.css" in source


def test_popup_should_define_compact_visual_structure():
    popup_source = POPUP_JS_PATH.read_text(
        encoding="utf-8"
    )

    assert "asset-popup__short-code" in popup_source
    assert "asset-popup__location" in popup_source
    assert "asset-popup__summary" in popup_source


def test_popup_styles_should_support_compact_layout():
    popup_css_path = (
        PROJECT_ROOT
        / "app"
        / "maps"
        / "static"
        / "css"
        / "popup.css"
    )

    source = popup_css_path.read_text(
        encoding="utf-8"
    )

    assert ".asset-popup__short-code" in source
    assert ".asset-popup__location" in source
    assert ".asset-popup__summary" in source
    assert "grid-template-columns: 1fr 1fr;" in source


def test_popup_should_not_keep_obsolete_visual_sections():
    popup_css_path = (
        PROJECT_ROOT
        / "app"
        / "maps"
        / "static"
        / "css"
        / "popup.css"
    )

    source = popup_css_path.read_text(
        encoding="utf-8"
    )

    assert ".asset-popup__health" not in source
    assert ".asset-popup__maintenance" not in source
    assert ".asset-popup__detail-icon" not in source
