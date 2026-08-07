"use strict";

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
function construirPopupActivo(activo) {
    const saludNumerica = Number(activo.salud);

    const saludValida = Number.isFinite(
        saludNumerica
    );

    const salud = saludValida
        ? Math.min(100, Math.max(0, saludNumerica))
        : 0;

    const textoSalud = saludValida
        ? `${salud}%`
        : "Sin evaluar";

    const claseEstado = obtenerClaseEstado(
        activo.estado
    );

    const iconoEstado = obtenerIconoEstado(
        activo.estado
    );

    return `
        <article class="asset-popup">

            <header class="asset-popup__header">

                <div class="asset-popup__identity">

                    <p class="asset-popup__eyebrow">
                        Activo industrial
                    </p>

                    <h3 class="asset-popup__title">
                        ${escaparHtml(activo.nombre)}
                    </h3>

                    <p class="asset-popup__code">
                        ${escaparHtml(activo.codigo)}
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
                        activo.estado || "Sin estado"
                    )}
                </span>

            </header>

            <div class="asset-popup__details">

                <div class="asset-popup__detail">

                    <span
                        class="asset-popup__detail-icon"
                        aria-hidden="true"
                    >
                        📍
                    </span>

                    <div>
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

                </div>

                <div class="asset-popup__detail">

                    <span
                        class="asset-popup__detail-icon"
                        aria-hidden="true"
                    >
                        🏭
                    </span>

                    <div>
                        <span class="asset-popup__label">
                            Área
                        </span>

                        <strong class="asset-popup__value">
                            ${escaparHtml(
                                activo.area
                                || "Sin área registrada"
                            )}
                        </strong>
                    </div>

                </div>

                <div class="asset-popup__detail">

                    <span
                        class="asset-popup__detail-icon"
                        aria-hidden="true"
                    >
                        ⚙️
                    </span>

                    <div>
                        <span class="asset-popup__label">
                            Modelo
                        </span>

                        <strong class="asset-popup__value">
                            ${escaparHtml(
                                activo.modelo
                                || "Sin modelo registrado"
                            )}
                        </strong>
                    </div>

                </div>

            </div>

            <section class="asset-popup__health">

                <div class="asset-popup__health-header">

                    <span class="asset-popup__label">
                        Salud del activo
                    </span>

                    <strong>
                        ${textoSalud}
                    </strong>

                </div>

                <div
                    class="asset-popup__health-track"
                    role="progressbar"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow="${salud}"
                    aria-label="Salud del activo"
                >
                    <span
                        class="asset-popup__health-fill"
                        style="width: ${salud}%"
                    ></span>
                </div>

            </section>

            <div class="asset-popup__maintenance">

                <div>
                    <span class="asset-popup__label">
                        Último mantenimiento
                    </span>

                    <strong class="asset-popup__value">
                        ${escaparHtml(
                            activo.ultimo_mantenimiento
                            || "Sin registro"
                        )}
                    </strong>
                </div>

                <div>
                    <span class="asset-popup__label">
                        Próximo mantenimiento
                    </span>

                    <strong class="asset-popup__value">
                        ${escaparHtml(
                            activo.proximo_mantenimiento
                            || "Sin programación"
                        )}
                    </strong>
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