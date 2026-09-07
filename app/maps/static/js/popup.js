"use strict";

let marcadorPopupActual = null;

/**
 * Convierte texto dinámico en contenido seguro para HTML.
 */
function escaparHtml(valor) {
    const elemento = document.createElement("div");

    elemento.textContent =
        valor === null || valor === undefined
            ? ""
            : String(valor);

    return elemento.innerHTML;
}


/**
 * Normaliza el estado para utilizarlo como clase CSS.
 */
function obtenerClaseEstado(estado) {
    const estadoNormalizado = String(
        estado || ""
    )
        .trim()
        .toLowerCase();

    const clases = {
        "operando": "asset-popup__status--operating",
        "advertencia": "asset-popup__status--warning",
        "falla": "asset-popup__status--failure",
        "fuera de servicio": "asset-popup__status--offline",
    };

    return (
        clases[estadoNormalizado]
        || "asset-popup__status--unknown"
    );
}


/**
 * Devuelve el indicador visual correspondiente al estado.
 */
function obtenerIconoEstado(estado) {
    const estadoNormalizado = String(
        estado || ""
    )
        .trim()
        .toLowerCase();

    const iconos = {
        "operando": "●",
        "advertencia": "●",
        "falla": "●",
        "fuera de servicio": "●",
    };

    return iconos[estadoNormalizado] || "●";
}


/**
 * Construye el contenido visual del popup.
 */
function obtenerCodigoCortoActivo(
    codigo
) {
    const codigoNormalizado =
        String(codigo || "").trim();

    if (!codigoNormalizado) {
        return "Sin codigo";
    }

    const partes =
        codigoNormalizado.split("-");

    return partes[
        partes.length - 1
    ].trim();
}


function construirPopupActivo(activo) {
    const codigoCorto =
        obtenerCodigoCortoActivo(
            activo.codigo
        );

    const tieneSalud =
        activo.salud !== null
        && activo.salud !== undefined
        && activo.salud !== "";

    const saludNumerica =
        tieneSalud
            ? Number(activo.salud)
            : Number.NaN;

    const saludValida =
        Number.isFinite(
            saludNumerica
        );

    const salud =
        saludValida
            ? Math.min(
                100,
                Math.max(
                    0,
                    saludNumerica
                )
            )
            : null;

    const textoSalud =
        salud !== null
            ? `${salud}%`
            : "Sin evaluar";

    const claseEstado =
        obtenerClaseEstado(
            activo.estado
        );

    const iconoEstado =
        obtenerIconoEstado(
            activo.estado
        );

    return `
        <article class="asset-popup">

            <header class="asset-popup__header">

                <div class="asset-popup__identity">

                    <h3 class="asset-popup__short-code">
                        ${escaparHtml(codigoCorto)}
                    </h3>

                    <p class="asset-popup__title">
                        ${escaparHtml(
                            activo.nombre
                            || "Activo sin nombre"
                        )}
                    </p>

                    <p class="asset-popup__code">
                        ${escaparHtml(
                            activo.codigo
                            || "Sin codigo"
                        )}
                    </p>

                </div>

                <span
                    class="
                        asset-popup__status
                        ${claseEstado}
                    "
                >
                    <span aria-hidden="true">
                        ${iconoEstado}
                    </span>

                    ${escaparHtml(
                        activo.estado
                        || "Sin estado"
                    )}
                </span>

            </header>

            <div class="asset-popup__details">

                <div class="
                    asset-popup__detail
                    asset-popup__location
                ">
                    <span class="asset-popup__label">
                        Ubicación
                    </span>

                    <strong class="asset-popup__value">
                        ${escaparHtml(
                            activo.ubicacion
                            || "Sin ubicación registrada"
                        )}
                    </strong>
                </div>

                <div class="asset-popup__summary">

                    <div class="asset-popup__detail">
                        <span class="asset-popup__label">
                            Área
                        </span>

                        <strong class="asset-popup__value">
                            ${escaparHtml(
                                activo.area
                                || "Sin Área registrada"
                            )}
                        </strong>
                    </div>

                    <div class="asset-popup__detail">
                        <span class="asset-popup__label">
                            Condición
                        </span>

                        <strong class="asset-popup__value">
                            ${textoSalud}
                        </strong>
                    </div>

                </div>

            </div>

            <footer class="asset-popup__actions">

                <button
                    type="button"
                    class="asset-popup__primary-action"
                    onclick="verMas(
                        '${escaparHtml(activo.codigo)}'
                    )"
                >
                    Abrir Hoja de Vida
                </button>

                <button
                    type="button"
                    class="asset-popup__secondary-action"
                    onclick="reubicarActivoDesdePopup()"
                >
                    Reubicar
                </button>

            </footer>

        </article>
    `;
}


/**
 * Consulta Assets y abre el popup del activo seleccionado.
 */
async function abrirPopup(
    elemento,
    assetCode,
    nombre
) {
    marcadorPopupActual = elemento;

    popup.style.display = "block";

    contenidoPopup.innerHTML = `
        <div class="asset-popup__loading">
            Cargando información de
            ${escaparHtml(nombre)}...
        </div>
    `;

    posicionarPopup(elemento);

    try {
        const response = await fetch(
            `/assets/api/${encodeURIComponent(assetCode)}`
        );

        if (!response.ok) {
            throw new Error(
                `Assets API respondió con ${response.status}`
            );
        }

        const activo = await response.json();

        contenidoPopup.innerHTML =
            construirPopupActivo(activo);

        posicionarPopup(elemento);

    } catch (error) {
        console.error(
            "No se pudo cargar el activo:",
            error
        );

        contenidoPopup.innerHTML = `
            <div class="asset-popup__error">

                <strong>
                    No fue posible cargar el activo.
                </strong>

                <span>
                    Intente nuevamente.
                </span>

            </div>
        `;
    }
}


/**
 * Coloca el popup sobre el marcador seleccionado.
 */
function posicionarPopup(elemento) {
    const rect = elemento.getBoundingClientRect();
    const mapaRect = mapa.getBoundingClientRect();

    popup.style.left = (
        rect.left
        - mapaRect.left
        + rect.width / 2
    ) + "px";

    popup.style.top = (
        rect.top
        - mapaRect.top
        - 8
    ) + "px";
}


/**
 * Inicia la reubicacion controlada del activo
 * mostrado actualmente en el popup.
 */
function reubicarActivoDesdePopup() {
    if (!marcadorPopupActual) {
        return;
    }

    iniciarReubicacionActivo(
        marcadorPopupActual
    );

    popup.style.display =
        "none";

    marcadorPopupActual =
        null;
}


/**
 * Abre la Hoja de Vida del activo.
 */
function verMas(codigo) {
    window.location.href =
        `/activo/${encodeURIComponent(codigo)}`;
}


const botonCerrar =
    document.getElementById("cerrarPopup");

if (botonCerrar) {

    botonCerrar.addEventListener(
        "click",
        () => {

            popup.style.display = "none";

        }
    );

}