from app.foundation.timeline.domain.timeline import Timeline
from app.foundation.timeline.services.timeline_service import TimelineService


timeline = Timeline()
service = TimelineService()

evento_1 = service.registrar_evento(
    timeline=timeline,
    categoria="Actividad",
    titulo="Actividad agregada",
    usuario="Fortunato Tenorio",
    descripcion="Preparar área de trabajo",
    icono="🛠",
    color="orange",
    referencia="OT-69926"
)

evento_2 = service.registrar_evento(
    timeline=timeline,
    categoria="Material",
    titulo="Material agregado",
    usuario="Daniel Hernández",
    descripcion="Cable THHN #12 — 20 m",
    icono="📦",
    color="blue",
    referencia="OT-69926"
)

print("Cantidad:", timeline.cantidad_eventos())

print("\nEVENTOS")

for evento in timeline.obtener_ordenados():
    print(
        evento.icono,
        evento.titulo,
        "-",
        evento.usuario,
        "-",
        evento.descripcion,
        "- Referencia:",
        evento.referencia
    )

print("\nPRIMER EVENTO CREADO")
print(evento_1.titulo if evento_1 else "No se creó")

print("\nSEGUNDO EVENTO CREADO")
print(evento_2.titulo if evento_2 else "No se creó")