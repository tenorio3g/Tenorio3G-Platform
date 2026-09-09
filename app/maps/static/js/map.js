"use strict";

const LOCATIONS_API_URL =
    "/maps/api/locations";

const LAYERS_API_URL =
    "/maps/api/layers";

const PLANS_API_URL =
    "/maps/api/plans";

const AVAILABLE_ASSETS_API_URL =
    "/maps/api/available-assets";

const mapa =
    document.getElementById("mapa");

const imagenMapa =
    document.getElementById("imagenMapa");

const mapViewport =
    mapa
        ? mapa.closest(".plant-map-viewport")
        : null;

const popup =
    document.getElementById("popup");

const contenidoPopup =
    document.getElementById("contenidoPopup");

const coordBox =
    document.getElementById("coordenadas");

const activoDisponible =
    document.getElementById("activoDisponible");

const categoriaPosicion =
    document.getElementById("categoriaPosicion");

const posicionSeleccionada =
    document.getElementById("posicionSeleccionada");

const guardarPosicion =
    document.getElementById("guardarPosicion");

const cancelarPosicion =
    document.getElementById("cancelarPosicion");

const editarMapa =
    document.getElementById("editarMapa");

const modoVisualizacionMapaControl =
    document.getElementById("modoVisualizacionMapa");

const mapLayerSelector =
    document.getElementById("mapLayerSelector");

const mapPlanSelector =
    document.getElementById("mapPlanSelector");

const estadoVisualizacionMapa =
    document.getElementById("estadoVisualizacionMapa");

const panelPosicionamientoMapa =
    document.getElementById("panelPosicionamientoMapa");

const mapRelocationOverlay =
    document.getElementById("mapRelocationOverlay");

const mapRelocationStatus =
    document.getElementById("mapRelocationStatus");

const guardarReubicacion =
    document.getElementById("guardarReubicacion");

const cancelarReubicacion =
    document.getElementById("cancelarReubicacion");


const estadoPosicion =
    document.getElementById("estadoPosicion");

const nivelZoomMapa =
    document.getElementById("nivelZoomMapa");

const restablecerVistaMapa =
    document.getElementById("restablecerVistaMapa");


const MIN_MAP_SCALE = 0.75;
const MAX_MAP_SCALE = 4;
const PAN_DRAG_THRESHOLD = 5;

const camera = {
    scale: 1,
    x: 0,
    y: 0,
};

let filtroCategoria = "todos";
let ubicaciones = [];
let capaActiva = null;
let planoActivo = null;

let posicionPendiente = null;
let marcadorProvisional = null;
let modoEdicionMapa = false;
let modoVisualizacionMapa = "all";
let codigoActivoBusqueda = null;

const modoUbicacion = {
    tipo: "place",
    assetCode: null,
    originalX: null,
    originalY: null,
};

const panState = {
    active: false,
    dragging: false,
    pointerId: null,
    startClientX: 0,
    startClientY: 0,
    startCameraX: 0,
    startCameraY: 0,
};

let ignorarSiguienteClickMapa = false;




function actualizarEstadoVisualizacionMapa() {
    if (!estadoVisualizacionMapa) {
        return;
    }

    if (modoVisualizacionMapa === "search") {
        if (codigoActivoBusqueda) {
            estadoVisualizacionMapa.textContent =
                `Solo busqueda \u00b7 Mostrando ${codigoActivoBusqueda}`;
            return;
        }

        estadoVisualizacionMapa.textContent =
            "Solo busqueda \u00b7 Mapa limpio \u00b7 Busca un activo para localizarlo";
        return;
    }

    estadoVisualizacionMapa.textContent =
        "Vista normal \u00b7 Mostrando todos los activos del filtro actual";
}



function cambiarModoVisualizacionMapa(modo) {
    modoVisualizacionMapa =
        modo === "search"
            ? "search"
            : "all";

    if (modoVisualizacionMapa === "search") {
        codigoActivoBusqueda = null;
        limpiarResultadosBusqueda();
    }

    renderPuntos(
        obtenerUbicacionesVisibles()
    );

    actualizarEstadoVisualizacionMapa();
}


function establecerModoEdicionMapa(activo) {
    modoEdicionMapa =
        Boolean(activo);

    if (
        !modoEdicionMapa
        && modoUbicacion.tipo === "place"
    ) {
        limpiarPosicionPendiente();
        restablecerModoUbicacion();

        actualizarEstadoPosicion(
            "Selecciona un activo y despues haz clic sobre el mapa."
        );
    }

    if (panelPosicionamientoMapa) {
        panelPosicionamientoMapa.hidden =
            !modoEdicionMapa;
    }

    if (editarMapa) {
        editarMapa.textContent =
            modoEdicionMapa
                ? "Salir de edicion"
                : "Editar mapa";

        editarMapa.setAttribute(
            "aria-expanded",
            String(modoEdicionMapa)
        );
    }
}


async function cargarPlanos() {
    if (!mapPlanSelector) {
        return;
    }

    try {
        const response = await fetch(
            PLANS_API_URL
        );

        if (!response.ok) {
            throw new Error(
                `Plans API respondio con ${response.status}`
            );
        }

        const plans =
            await response.json();

        mapPlanSelector.replaceChildren();

        if (plans.length === 0) {
            planoActivo = null;

            const option =
                document.createElement("option");

            option.value = "";
            option.textContent =
                "Sin planos disponibles";

            mapPlanSelector.appendChild(
                option
            );

            mapPlanSelector.disabled = true;
            return;
        }

        plans.forEach(
            plan => {
                const option =
                    document.createElement("option");

                option.value =
                    plan.code;

                option.textContent =
                    plan.name;

                mapPlanSelector.appendChild(
                    option
                );
            }
        );

        mapPlanSelector.disabled = false;

        planoActivo =
            plans[0].code;

        mapPlanSelector.value =
            planoActivo;

    } catch (error) {
        console.error(
            "Error cargando planos:",
            error
        );

        planoActivo = null;

        mapPlanSelector.replaceChildren();

        const option =
            document.createElement("option");

        option.value = "";
        option.textContent =
            "Error cargando planos";

        mapPlanSelector.appendChild(
            option
        );

        mapPlanSelector.disabled = true;
    }
}


async function cargarCapas() {
    if (!mapLayerSelector) {
        return;
    }

    try {
        const response = await fetch(
            LAYERS_API_URL
        );

        if (!response.ok) {
            throw new Error(
                `Layers API respondio con ${response.status}`
            );
        }

        const layers =
            await response.json();

        mapLayerSelector.replaceChildren();

        if (layers.length === 0) {
            capaActiva = null;

            const option =
                document.createElement("option");

            option.value = "";
            option.textContent =
                "Sin capas disponibles";

            mapLayerSelector.appendChild(
                option
            );

            mapLayerSelector.disabled = true;
            return;
        }

        layers.forEach(
            layer => {
                const option =
                    document.createElement("option");

                option.value =
                    layer.code;

                option.textContent =
                    layer.name;

                mapLayerSelector.appendChild(
                    option
                );
            }
        );

        mapLayerSelector.disabled = false;

        capaActiva =
            layers[0].code;

        mapLayerSelector.value =
            capaActiva;

    } catch (error) {
        console.error(
            "Error cargando capas:",
            error
        );

        capaActiva = null;

        mapLayerSelector.replaceChildren();

        const option =
            document.createElement("option");

        option.value = "";
        option.textContent =
            "Error cargando capas";

        mapLayerSelector.appendChild(
            option
        );

        mapLayerSelector.disabled = true;
    }
}


async function cargarUbicaciones() {
    try {
        const response = await fetch(
            LOCATIONS_API_URL
        );

        if (!response.ok) {
            throw new Error(
                `Maps API respondio con ${response.status}`
            );
        }

        ubicaciones = await response.json();

        renderPuntos(
            obtenerUbicacionesVisibles()
        );

    } catch (error) {
        console.error(
            "Error cargando ubicaciones:",
            error
        );
    }
}


async function cargarActivosDisponibles() {
    if (!activoDisponible) {
        return;
    }

    try {
        const response = await fetch(
            AVAILABLE_ASSETS_API_URL
        );

        if (!response.ok) {
            throw new Error(
                `Assets API respondio con ${response.status}`
            );
        }

        const assets = await response.json();

        activoDisponible.innerHTML = "";

        const emptyOption =
            document.createElement("option");

        emptyOption.value = "";

        if (assets.length === 0) {
            emptyOption.textContent =
                "No hay activos pendientes de posicionar";

            activoDisponible.appendChild(
                emptyOption
            );

            activoDisponible.disabled = true;

            actualizarEstadoPosicion(
                "Todos los activos disponibles ya tienen posicion en el mapa."
            );

            return;
        }

        activoDisponible.disabled = false;

        emptyOption.textContent =
            "Selecciona un activo";

        activoDisponible.appendChild(
            emptyOption
        );

        assets.forEach(asset => {
            const option =
                document.createElement("option");

            option.value = asset.code;
            option.textContent =
                `${asset.code} - ${asset.name}`;

            activoDisponible.appendChild(
                option
            );
        });

    } catch (error) {
        console.error(
            "Error cargando activos disponibles:",
            error
        );

        activoDisponible.innerHTML =
            '<option value="">Error al cargar activos</option>';

        activoDisponible.disabled = true;

        actualizarEstadoPosicion(
            "No fue posible cargar los activos disponibles.",
            true
        );
    }
}


function obtenerUbicacionesFiltradas() {
    return ubicaciones.filter(
        location => {
            const perteneceAPlano =
                location.plan_code === planoActivo;

            const perteneceACapa =
                location.layer_code === capaActiva;

            const perteneceACategoria =
                filtroCategoria === "todos"
                || location.category
                    === filtroCategoria;

            return (
                perteneceAPlano
                && perteneceACapa
                && perteneceACategoria
            );
        }
    );
}



function obtenerUbicacionesVisibles() {
    if (modoVisualizacionMapa === "search") {
        if (!codigoActivoBusqueda) {
            return [];
        }

        return ubicaciones.filter(
            location =>
                location.plan_code === planoActivo
                && location.layer_code === capaActiva
                && location.asset_code
                    === codigoActivoBusqueda
        );
    }

    return obtenerUbicacionesFiltradas();
}


function renderPuntos(locations) {
    mapa.querySelectorAll(
        ".punto"
    ).forEach(
        punto => punto.remove()
    );

    locations.forEach(data => {
        const punto =
            document.createElement("div");

        punto.className =
            "punto "
            + (data.category || "default");

        punto.style.left =
            data.x + "%";

        punto.style.top =
            data.y + "%";

        punto.title =
            data.name;

        punto.dataset.codigo =
            data.asset_code || "";

        punto.dataset.nombre =
            data.name || "";

        punto.addEventListener(
            "click",
            event => {
                event.stopPropagation();

                abrirPopup(
                    punto,
                    data.asset_code,
                    data.name
                );
            }
        );

        mapa.appendChild(
            punto
        );
    });
}


function limitarEscalaMapa(scale) {
    return Math.min(
        MAX_MAP_SCALE,
        Math.max(
            MIN_MAP_SCALE,
            scale
        )
    );
}


function actualizarIndicadorZoom() {
    if (!nivelZoomMapa) {
        return;
    }

    nivelZoomMapa.textContent =
        `${Math.round(camera.scale * 100)}%`;
}


function aplicarCamara() {
    if (!mapa) {
        return;
    }

    mapa.style.transform =
        `translate(${camera.x}px, ${camera.y}px) `
        + `scale(${camera.scale})`;

    actualizarIndicadorZoom();
}


function restablecerCamaraMapa() {
    camera.scale = 1;
    camera.x = 0;
    camera.y = 0;

    aplicarCamara();
}


function manejarZoomRueda(event) {
    if (!mapViewport) {
        return;
    }

    event.preventDefault();

    const viewportRect =
        mapViewport.getBoundingClientRect();

    const pointerX =
        event.clientX - viewportRect.left;

    const pointerY =
        event.clientY - viewportRect.top;

    const previousScale =
        camera.scale;

    const zoomFactor =
        event.deltaY < 0
            ? 1.12
            : 1 / 1.12;

    const nextScale =
        limitarEscalaMapa(
            previousScale * zoomFactor
        );

    if (nextScale === previousScale) {
        return;
    }

    const mapX = (
        pointerX - camera.x
    ) / previousScale;

    const mapY = (
        pointerY - camera.y
    ) / previousScale;

    camera.scale = nextScale;

    camera.x =
        pointerX - mapX * nextScale;

    camera.y =
        pointerY - mapY * nextScale;

    aplicarCamara();
}


function iniciarPanMapa(event) {
    if (
        event.button !== 0
        || event.target.closest(
            ".punto, .map-popup"
        )
    ) {
        return;
    }

    panState.active = true;
    panState.dragging = false;
    panState.pointerId = event.pointerId;

    panState.startClientX =
        event.clientX;

    panState.startClientY =
        event.clientY;

    panState.startCameraX =
        camera.x;

    panState.startCameraY =
        camera.y;

    mapa.classList.add(
        "is-pan-ready"
    );

}


function moverPanMapa(event) {
    if (
        !panState.active
        || event.pointerId
            !== panState.pointerId
    ) {
        return;
    }

    const deltaX =
        event.clientX
        - panState.startClientX;

    const deltaY =
        event.clientY
        - panState.startClientY;

    const distance =
        Math.hypot(
            deltaX,
            deltaY
        );

    if (
        !panState.dragging
        && distance < PAN_DRAG_THRESHOLD
    ) {
        return;
    }

    if (!panState.dragging) {
        panState.dragging = true;

        mapa.classList.remove(
            "is-pan-ready"
        );

        mapa.classList.add(
            "is-panning"
        );
    }

    camera.x =
        panState.startCameraX
        + deltaX;

    camera.y =
        panState.startCameraY
        + deltaY;

    aplicarCamara();
}


function finalizarPanMapa(event) {
    if (
        !panState.active
        || event.pointerId
            !== panState.pointerId
    ) {
        return;
    }

    const wasDragging =
        panState.dragging;

    panState.active = false;
    panState.dragging = false;
    panState.pointerId = null;

    mapa.classList.remove(
        "is-pan-ready",
        "is-panning"
    );

    if (wasDragging) {
        ignorarSiguienteClickMapa = true;
    }
}


function enfocarActivoMapa(punto) {
    if (
        !mapViewport
        || !mapa
        || !punto
    ) {
        return;
    }

    const viewportRect =
        mapViewport.getBoundingClientRect();

    const mapWidth =
        mapa.offsetWidth;

    const mapHeight =
        mapa.offsetHeight;

    if (
        mapWidth <= 0
        || mapHeight <= 0
    ) {
        return;
    }

    const leftPercent =
        Number.parseFloat(
            punto.style.left
        );

    const topPercent =
        Number.parseFloat(
            punto.style.top
        );

    if (
        !Number.isFinite(leftPercent)
        || !Number.isFinite(topPercent)
    ) {
        return;
    }

    const assetX =
        mapWidth
        * leftPercent
        / 100;

    const assetY =
        mapHeight
        * topPercent
        / 100;

    const viewportCenterX =
        viewportRect.width / 2;

    const viewportCenterY =
        viewportRect.height / 2;

    camera.x =
        viewportCenterX
        - assetX * camera.scale;

    camera.y =
        viewportCenterY
        - assetY * camera.scale;

    aplicarCamara();
}


function obtenerIdentificadorCorto(codigo) {
    if (!codigo) {
        return "";
    }

    return codigo
        .split("-")
        .pop()
        .trim()
        .toUpperCase();
}


function limpiarResultadosBusqueda() {
    const contenedor =
        document.getElementById(
            "resultadosBusquedaMapa"
        );

    if (!contenedor) {
        return;
    }

    contenedor.replaceChildren();
    contenedor.hidden = true;
}



function limpiarEnfoqueBusqueda() {
    mapa.querySelectorAll(
        ".punto"
    ).forEach(
        punto => punto.classList.remove(
            "parpadeo"
        )
    );
}


function obtenerCoincidenciasBusqueda(texto) {
    return ubicaciones.filter(
        location => {
            const codigo = (
                location.asset_code
                || ""
            ).toLowerCase();

            const nombre = (
                location.name
                || ""
            ).toLowerCase();

            const identificadorCorto =
                obtenerIdentificadorCorto(
                    location.asset_code
                ).toLowerCase();

            return (
                codigo.includes(texto)
                || identificadorCorto.includes(texto)
                || nombre.includes(texto)
            );
        }
    );
}





function seleccionarResultadoBusqueda(location) {
    codigoActivoBusqueda =
        location.asset_code;

    const cambioDePlano =
        location.plan_code
        && location.plan_code !== planoActivo;

    const cambioDeCapa =
        location.layer_code
        && location.layer_code !== capaActiva;

    if (cambioDePlano) {
        planoActivo = location.plan_code;

        if (mapPlanSelector) {
            mapPlanSelector.value = planoActivo;
        }

        actualizarImagenPlano(
            planoActivo
        );

        restablecerCamaraMapa();
    }

    if (cambioDeCapa) {
        capaActiva = location.layer_code;

        if (mapLayerSelector) {
            mapLayerSelector.value = capaActiva;
        }
    }

    if (
        modoVisualizacionMapa === "search"
        || cambioDePlano
        || cambioDeCapa
    ) {
        renderPuntos(
            obtenerUbicacionesVisibles()
        );
    }

    limpiarEnfoqueBusqueda();

    const punto = Array.from(
        mapa.querySelectorAll(".punto")
    ).find(
        item =>
            item.dataset.codigo
            === location.asset_code
    );

    if (!punto) {
        actualizarEstadoVisualizacionMapa();
        return;
    }

    punto.classList.add(
        "is-search-match"
    );

    punto.classList.add(
        "parpadeo"
    );

    enfocarActivoMapa(
        punto
    );

    limpiarResultadosBusqueda();
    actualizarEstadoVisualizacionMapa();
}



function mostrarResultadosBusqueda(coincidencias) {
    const contenedor =
        document.getElementById(
            "resultadosBusquedaMapa"
        );

    if (!contenedor) {
        return;
    }

    contenedor.replaceChildren();

    const encabezado =
        document.createElement("div");

    encabezado.className =
        "map-search-results__header";

    encabezado.textContent =
        `${coincidencias.length} coincidencias encontradas`;

    contenedor.appendChild(
        encabezado
    );

    coincidencias.forEach(
        location => {
            const boton =
                document.createElement("button");

            boton.type = "button";
            boton.className =
                "map-search-result";

            const identificador =
                document.createElement("strong");

            identificador.className =
                "map-search-result__identifier";

            identificador.textContent =
                obtenerIdentificadorCorto(
                    location.asset_code
                );

            const nombre =
                document.createElement("span");

            nombre.className =
                "map-search-result__name";

            nombre.textContent =
                location.name
                || "Activo sin nombre";

            const codigo =
                document.createElement("small");

            codigo.className =
                "map-search-result__code";

            codigo.textContent =
                location.asset_code
                || "";

            boton.appendChild(
                identificador
            );

            boton.appendChild(
                nombre
            );

            boton.appendChild(
                codigo
            );

            boton.addEventListener(
                "click",
                () => {
                    seleccionarResultadoBusqueda(
                        location
                    );
                }
            );

            contenedor.appendChild(
                boton
            );
        }
    );

    contenedor.hidden = false;
}



function buscarEquipo() {
    const campo =
        document.getElementById(
            "busqueda"
        );

    if (!campo) {
        return;
    }

    cerrarPopup();

    const texto =
        campo.value
            .toLowerCase()
            .trim();

    limpiarResultadosBusqueda();

    limpiarEnfoqueBusqueda();

    if (texto === "") {
        return;
    }

    const coincidencias =
        obtenerCoincidenciasBusqueda(texto);

    if (coincidencias.length === 0) {
        alert(
            "Equipo no encontrado"
        );
        return;
    }

    if (coincidencias.length === 1) {
        seleccionarResultadoBusqueda(
            coincidencias[0]
        );
        return;
    }

    mostrarResultadosBusqueda(
        coincidencias
    );
}


function zoomMapa(factor) {
    camera.scale = limitarEscalaMapa(
        camera.scale * factor
    );

    aplicarCamara();
}


function obtenerImagenPlano(planCode) {
    if (!imagenMapa) {
        return null;
    }

    const imagenesPorPlano = {
        ground_floor:
            imagenMapa.dataset.planGroundFloor,
        upper_floor:
            imagenMapa.dataset.planUpperFloor,
        roof:
            imagenMapa.dataset.planRoof,
    };

    return (
        imagenesPorPlano[planCode]
        || imagenMapa.dataset.planGroundFloor
        || null
    );
}


function actualizarImagenPlano(planCode) {
    if (!imagenMapa) {
        return;
    }

    const imageUrl =
        obtenerImagenPlano(planCode);

    if (!imageUrl) {
        return;
    }

    imagenMapa.src = imageUrl;
    imagenMapa.alt =
        `Plano ${planCode || "sin seleccionar"}`;
}


if (imagenMapa) {
    imagenMapa.addEventListener(
        "error",
        () => {
            const fallbackUrl =
                imagenMapa.dataset.planGroundFloor;

            if (
                fallbackUrl
                && imagenMapa.src !== fallbackUrl
            ) {
                imagenMapa.src = fallbackUrl;
            }
        }
    );
}


function cambiarPlanoMapa(planCode) {
    planoActivo =
        planCode || null;

    codigoActivoBusqueda = null;

    limpiarResultadosBusqueda();
    limpiarEnfoqueBusqueda();

    actualizarImagenPlano(
        planoActivo
    );

    restablecerCamaraMapa();

    renderPuntos(
        obtenerUbicacionesVisibles()
    );

    actualizarEstadoVisualizacionMapa();
}


function cambiarCapaMapa(layerCode) {
    capaActiva =
        layerCode || null;

    codigoActivoBusqueda = null;

    limpiarResultadosBusqueda();
    limpiarEnfoqueBusqueda();

    renderPuntos(
        obtenerUbicacionesVisibles()
    );

    actualizarEstadoVisualizacionMapa();
}


function cambiarCategoria(categoria) {
    filtroCategoria = categoria;

    renderPuntos(
        obtenerUbicacionesVisibles()
    );
}


function obtenerCoordenadasMapa(event) {
    const rect =
        mapa.getBoundingClientRect();

    const x = (
        (
            event.clientX
            - rect.left
        )
        / rect.width
        * 100
    );

    const y = (
        (
            event.clientY
            - rect.top
        )
        / rect.height
        * 100
    );

    return {
        x: Number(
            x.toFixed(1)
        ),
        y: Number(
            y.toFixed(1)
        ),
    };
}


function mostrarControlesReubicacion(
    assetCode
) {
    if (
        !mapRelocationOverlay
        || !mapRelocationStatus
    ) {
        return;
    }

    mapRelocationStatus.textContent =
        `Reubicando ${assetCode}. `
        + "Selecciona la nueva posicion.";

    mapRelocationOverlay.hidden =
        false;

    if (guardarReubicacion) {
        guardarReubicacion.disabled =
            true;
    }
}


function actualizarControlesReubicacion(
    coordinates
) {
    if (
        !mapRelocationStatus
        || !coordinates
    ) {
        return;
    }

    const assetCode =
        modoUbicacion.assetCode
        || "Activo";

    mapRelocationStatus.textContent =
        `${assetCode} ? Nueva posicion `
        + `X: ${coordinates.x.toFixed(2)}%, `
        + `Y: ${coordinates.y.toFixed(2)}%`;

    if (guardarReubicacion) {
        guardarReubicacion.disabled =
            false;
    }
}


function ocultarControlesReubicacion() {
    if (mapRelocationOverlay) {
        mapRelocationOverlay.hidden =
            true;
    }

    if (guardarReubicacion) {
        guardarReubicacion.disabled =
            true;
    }
}


function iniciarReubicacionActivo(
    punto
) {
    if (!punto) {
        return;
    }

    const assetCode =
        punto.dataset.codigo
        || "";

    const originalX =
        Number.parseFloat(
            punto.style.left
        );

    const originalY =
        Number.parseFloat(
            punto.style.top
        );

    if (
        !assetCode
        || !Number.isFinite(originalX)
        || !Number.isFinite(originalY)
    ) {
        return;
    }

    limpiarPosicionPendiente();

    modoUbicacion.tipo =
        "move";

    modoUbicacion.assetCode =
        assetCode;

    modoUbicacion.originalX =
        originalX;

    modoUbicacion.originalY =
        originalY;

    mostrarControlesReubicacion(
        assetCode
    );

    actualizarEstadoPosicion(
        `Reubicando ${assetCode}. `
        + "Selecciona la nueva posicion."
    );
}


function restablecerModoUbicacion() {
    modoUbicacion.tipo =
        "place";

    modoUbicacion.assetCode =
        null;

    modoUbicacion.originalX =
        null;

    modoUbicacion.originalY =
        null;
}


function obtenerActivoParaPosicion() {
    if (
        modoUbicacion.tipo === "move"
    ) {
        return modoUbicacion.assetCode;
    }

    if (!activoDisponible) {
        return "";
    }

    return activoDisponible.value;
}


function seleccionarPosicion(event) {
    if (ignorarSiguienteClickMapa) {
        ignorarSiguienteClickMapa = false;
        return;
    }

    const assetCode =
        obtenerActivoParaPosicion();

    if (!assetCode) {
        actualizarEstadoPosicion(
            "Selecciona primero un activo.",
            true
        );

        return;
    }

    if (
        modoUbicacion.tipo === "move"
        && !modoUbicacion.assetCode
    ) {
        actualizarEstadoPosicion(
            "No hay un activo seleccionado para reubicar.",
            true
        );

        return;
    }

    if (
        event.target.closest(
            ".punto, .map-popup"
        )
    ) {
        return;
    }

    const coordinates =
        obtenerCoordenadasMapa(event);

    posicionPendiente =
        coordinates;

    mostrarMarcadorProvisional(
        coordinates
    );

    if (
        modoUbicacion.tipo === "move"
    ) {
        actualizarControlesReubicacion(
            coordinates
        );
    }

    posicionSeleccionada.textContent =
        `X: ${coordinates.x}%, Y: ${coordinates.y}%`;

    guardarPosicion.disabled =
        false;

    cancelarPosicion.disabled =
        false;

    actualizarEstadoPosicion(
        "Posicion seleccionada. Confirma con Guardar posicion."
    );
}


function mostrarMarcadorProvisional(
    coordinates
) {
    eliminarMarcadorProvisional();

    marcadorProvisional =
        document.createElement("div");

    marcadorProvisional.className =
        "punto punto-preview";

    marcadorProvisional.style.left =
        coordinates.x + "%";

    marcadorProvisional.style.top =
        coordinates.y + "%";

    mapa.appendChild(
        marcadorProvisional
    );
}


function eliminarMarcadorProvisional() {
    if (!marcadorProvisional) {
        return;
    }

    marcadorProvisional.remove();
    marcadorProvisional = null;
}


function limpiarPosicionPendiente() {
    posicionPendiente = null;

    eliminarMarcadorProvisional();

    if (posicionSeleccionada) {
        posicionSeleccionada.textContent =
            "X: --%, Y: --%";
    }

    if (guardarPosicion) {
        guardarPosicion.disabled =
            true;
    }

    if (cancelarPosicion) {
        cancelarPosicion.disabled =
            true;
    }
}


async function guardarPosicionSeleccionada() {
    const assetCode =
        obtenerActivoParaPosicion();

    if (
        !assetCode
        || !posicionPendiente
    ) {
        actualizarEstadoPosicion(
            "Selecciona un activo y una posicion.",
            true
        );

        return;
    }

    const isMove =
        modoUbicacion.tipo === "move";

    const requestUrl =
        isMove
            ? `${LOCATIONS_API_URL}/${encodeURIComponent(
                assetCode
            )}`
            : LOCATIONS_API_URL;

    let requestOptions;

    if (isMove) {
        requestOptions = {
            method: "PATCH",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                {
                    x:
                        posicionPendiente.x,
                    y:
                        posicionPendiente.y,
                }
            ),
        };
    } else {
        requestOptions = {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(
                {
                    asset_code:
                        assetCode,
                    category:
                        categoriaPosicion.value,
                    layer_code:
                        capaActiva,
                    plan_code:
                        planoActivo,
                    x:
                        posicionPendiente.x,
                    y:
                        posicionPendiente.y,
                }
            ),
        };
    }

    guardarPosicion.disabled =
        true;

    actualizarEstadoPosicion(
        isMove
            ? "Guardando nueva ubicacion..."
            : "Guardando posicion..."
    );

    try {
        const response = await fetch(
            requestUrl,
            requestOptions
        );

        const payload =
            await response.json();

        if (!response.ok) {
            throw new Error(
                payload.message
                || (
                    isMove
                        ? "No fue posible reubicar el activo."
                        : "No fue posible guardar la posicion."
                )
            );
        }

        limpiarPosicionPendiente();

        if (isMove) {
            restablecerModoUbicacion();
            ocultarControlesReubicacion();
        }

        actualizarEstadoPosicion(
            payload.message
        );

        await cargarUbicaciones();
        await cargarActivosDisponibles();

    } catch (error) {
        console.error(
            isMove
                ? "Error reubicando activo:"
                : "Error guardando posicion:",
            error
        );

        guardarPosicion.disabled =
            false;

        actualizarEstadoPosicion(
            error.message,
            true
        );
    }
}


function actualizarEstadoPosicion(
    message,
    isError = false
) {
    if (!estadoPosicion) {
        return;
    }

    estadoPosicion.textContent =
        message;

    estadoPosicion.classList.toggle(
        "is-error",
        isError
    );
}


if (coordBox) {
    mapa.addEventListener(
        "mousemove",
        event => {
            const coordinates =
                obtenerCoordenadasMapa(
                    event
                );

            coordBox.textContent =
                `X: ${coordinates.x}%, Y: ${coordinates.y}%`;
        }
    );
}


const campoBusqueda =
    document.getElementById("busqueda");

if (campoBusqueda) {
    campoBusqueda.addEventListener(
        "keydown",
        (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                buscarEquipo();
            }
        }
    );
}


if (mapa) {
    mapa.addEventListener(
        "click",
        seleccionarPosicion
    );

    mapa.addEventListener(
        "pointerdown",
        iniciarPanMapa
    );

}


window.addEventListener(
    "pointermove",
    moverPanMapa
);

window.addEventListener(
    "pointerup",
    finalizarPanMapa
);

window.addEventListener(
    "pointercancel",
    finalizarPanMapa
);


if (mapViewport) {
    mapViewport.addEventListener(
        "wheel",
        manejarZoomRueda,
        {
            passive: false,
        }
    );
}


if (mapPlanSelector) {
    mapPlanSelector.addEventListener(
        "change",
        () => {
            cambiarPlanoMapa(
                mapPlanSelector.value
            );
        }
    );
}


if (mapLayerSelector) {
    mapLayerSelector.addEventListener(
        "change",
        () => {
            cambiarCapaMapa(
                mapLayerSelector.value
            );
        }
    );
}


if (modoVisualizacionMapaControl) {
    modoVisualizacionMapaControl.addEventListener(
        "change",
        () => {
            cambiarModoVisualizacionMapa(
                modoVisualizacionMapaControl.value
            );
        }
    );
}


if (editarMapa) {
    editarMapa.addEventListener(
        "click",
        () => {
            establecerModoEdicionMapa(
                !modoEdicionMapa
            );
        }
    );
}


if (guardarPosicion) {
    guardarPosicion.addEventListener(
        "click",
        guardarPosicionSeleccionada
    );
}


if (cancelarPosicion) {
    cancelarPosicion.addEventListener(
        "click",
        () => {
            limpiarPosicionPendiente();
            restablecerModoUbicacion();

            actualizarEstadoPosicion(
                "Selecciona una nueva posicion sobre el mapa."
            );
        }
    );
}


if (guardarReubicacion) {
    guardarReubicacion.addEventListener(
        "click",
        guardarPosicionSeleccionada
    );
}


if (cancelarReubicacion) {
    cancelarReubicacion.addEventListener(
        "click",
        () => {
            limpiarPosicionPendiente();
            restablecerModoUbicacion();
            ocultarControlesReubicacion();

            actualizarEstadoPosicion(
                "Selecciona una nueva posicion sobre el mapa."
            );
        }
    );
}


if (restablecerVistaMapa) {
    restablecerVistaMapa.addEventListener(
        "click",
        restablecerCamaraMapa
    );
}


if (activoDisponible) {
    activoDisponible.addEventListener(
        "change",
        () => {
            limpiarPosicionPendiente();

            if (activoDisponible.value) {
                actualizarEstadoPosicion(
                    "Ahora haz clic sobre el mapa para elegir la posicion."
                );
            } else {
                actualizarEstadoPosicion(
                    "Selecciona un activo y despues haz clic sobre el mapa."
                );
            }
        }
    );
}


async function inicializarMapa() {
    await cargarPlanos();
    await cargarCapas();
    await cargarUbicaciones();
    await cargarActivosDisponibles();
}


aplicarCamara();

inicializarMapa();
