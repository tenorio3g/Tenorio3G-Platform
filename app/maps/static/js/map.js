"use strict";

const LOCATIONS_API_URL =
    "/maps/api/locations";

const AVAILABLE_ASSETS_API_URL =
    "/maps/api/available-assets";

const mapa =
    document.getElementById("mapa");

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

let posicionPendiente = null;
let marcadorProvisional = null;

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
            obtenerUbicacionesFiltradas()
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
    if (filtroCategoria === "todos") {
        return ubicaciones;
    }

    return ubicaciones.filter(
        location =>
            location.category === filtroCategoria
    );
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


function buscarEquipo() {
    const texto = document
        .getElementById("busqueda")
        .value
        .toLowerCase()
        .trim();

    let encontrado = false;

    mapa.querySelectorAll(
        ".punto"
    ).forEach(
        punto =>
            punto.classList.remove(
                "parpadeo"
            )
    );

    mapa.querySelectorAll(
        ".punto"
    ).forEach(
        punto => {
            if (
                punto.title
                    .toLowerCase()
                    .includes(texto)
                && texto !== ""
            ) {
                punto.classList.add(
                    "parpadeo"
                );

                encontrado = true;

                // El centrado automatico del activo
                // se implementara en MAP-UX-002.
            }
        }
    );

    if (
        !encontrado
        && texto !== ""
    ) {
        alert(
            "Equipo no encontrado"
        );
    }
}


function zoomMapa(factor) {
    camera.scale = limitarEscalaMapa(
        camera.scale * factor
    );

    aplicarCamara();
}


function cambiarCategoria(categoria) {
    filtroCategoria = categoria;

    renderPuntos(
        obtenerUbicacionesFiltradas()
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


function seleccionarPosicion(event) {
    if (ignorarSiguienteClickMapa) {
        ignorarSiguienteClickMapa = false;
        return;
    }

    if (
        !activoDisponible
        || !activoDisponible.value
    ) {
        actualizarEstadoPosicion(
            "Selecciona primero un activo.",
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
    if (
        !activoDisponible.value
        || !posicionPendiente
    ) {
        actualizarEstadoPosicion(
            "Selecciona un activo y una posicion.",
            true
        );

        return;
    }

    guardarPosicion.disabled =
        true;

    actualizarEstadoPosicion(
        "Guardando posicion..."
    );

    try {
        const response = await fetch(
            LOCATIONS_API_URL,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json",
                },
                body: JSON.stringify(
                    {
                        asset_code:
                            activoDisponible.value,
                        category:
                            categoriaPosicion.value,
                        x:
                            posicionPendiente.x,
                        y:
                            posicionPendiente.y,
                    }
                ),
            }
        );

        const payload =
            await response.json();

        if (!response.ok) {
            throw new Error(
                payload.message
                || "No fue posible guardar la posicion."
            );
        }

        limpiarPosicionPendiente();

        actualizarEstadoPosicion(
            payload.message
        );

        await cargarUbicaciones();
        await cargarActivosDisponibles();

    } catch (error) {
        console.error(
            "Error guardando posicion:",
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


aplicarCamara();

cargarUbicaciones();
cargarActivosDisponibles();
