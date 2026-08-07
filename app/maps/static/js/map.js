// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBW_fvQaubSplkMGGlrSWcszpBsnxML_iA",
  authDomain: "equipos-beaf1.firebaseapp.com",
  projectId: "equipos-beaf1",
  storageBucket: "equipos-beaf1.appspot.com",
  messagingSenderId: "190150028300",
  appId: "1:190150028300:web:df3a8d191a884e4974d229"
};
// ==========================================
// Tenorio3G API
// ==========================================

const API_URL = "/maps/api/locations";

const mapa = document.getElementById("mapa");
const popup = document.getElementById("popup");
const contenidoPopup = document.getElementById("contenidoPopup");
let escalaMapa = 1;
let filtroCategoria = "todos";

// ==========================================
// Cargar ubicaciones desde Tenorio3G
// ==========================================

async function cargarUbicaciones() {

    try {

        const response = await fetch(API_URL);

        console.log(response);

        const locations = await response.json();

        console.log(locations);

        renderPuntos(locations);

    }
    catch(error){

        console.error("Error cargando ubicaciones:", error);

    }

}
cargarUbicaciones();

function renderPuntos(locations) {

    mapa.querySelectorAll(".punto").forEach(
        p => p.remove()
    );

    locations.forEach(data => {

        if (
            filtroCategoria !== "todos"
            &&
            data.category !== filtroCategoria
        ){
            return;
        }

        const punto = document.createElement("div");

        punto.className =
            "punto " +
            (data.category || "default");

        punto.style.left = data.x + "%";

        punto.style.top = data.y + "%";

        punto.title = data.name;

        punto.onclick = () =>
            abrirPopup(
                punto,
                data.asset_code,
                data.name
            );

        mapa.appendChild(punto);

    });

}



// Buscar equipo
function buscarEquipo() {
  const texto = document.getElementById("busqueda").value.toLowerCase().trim();
  let encontrado = false;
  mapa.querySelectorAll(".punto").forEach(p => p.classList.remove("parpadeo"));
  
  mapa.querySelectorAll(".punto").forEach(p => {
    if (p.title.toLowerCase() === texto) {
      p.classList.add("parpadeo");
      encontrado = true;
      // Calcular centro del punto
      const rectMapa = mapa.getBoundingClientRect();
      const rectPunto = p.getBoundingClientRect();
      const offsetX = ((rectPunto.left + rectPunto.width/2) - rectMapa.left) / rectMapa.width * 100;
      const offsetY = ((rectPunto.top + rectPunto.height/2) - rectMapa.top) / rectMapa.height * 100;

      // Cambiar origen de zoom al punto buscado
      mapa.style.transformOrigin = `${offsetX}% ${offsetY}%`;

      // Forzar pequeño zoom in/out para centrar visualmente
      mapa.style.transform = `scale(${escalaMapa})`;
    }
  });

  if (!encontrado && texto !== "") alert("Equipo no encontrado");
}

// Zoom
function zoomMapa(factor) {
  escalaMapa *= factor;
  mapa.style.transform = `scale(${escalaMapa})`;
}

// Filtro de categoría
function cambiarCategoria(cat) {
  filtroCategoria = cat;
  db.collection("equipos").get().then(renderPuntos);
}

// Mostrar coordenadas
const coordBox = document.getElementById("coordenadas");
mapa.addEventListener("mousemove", e => {
  const rect = mapa.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1);
  const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1);
  coordBox.textContent = `X: ${x}%, Y: ${y}%`;
});
