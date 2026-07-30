from datetime import datetime, timedelta

from app.foundation.timeline.domain.timeline import Timeline
from app.foundation.timeline.domain.timeline_event import TimelineEvent


timeline = Timeline()

evento_1 = TimelineEvent(
    categoria="Técnico",
    titulo="Técnico asignado",
    usuario="Fortunato Tenorio",
    descripcion="Daniel Hernández",
    icono="👷",
    color="blue",
    fecha=datetime.now() - timedelta(hours=2)
)

evento_2 = TimelineEvent(
    categoria="Actividad",
    titulo="Actividad agregada",
    usuario="Fortunato Tenorio",
    descripcion="Preparar área de trabajo",
    icono="🛠",
    color="orange",
    fecha=datetime.now() - timedelta(hours=1)
)

evento_3 = TimelineEvent(
    categoria="Estado",
    titulo="Orden iniciada",
    usuario="Daniel Hernández",
    descripcion="Asignada → En Proceso",
    icono="▶",
    color="green"
)

timeline.agregar_evento(evento_1)
timeline.agregar_evento(evento_2)
timeline.agregar_evento(evento_3)

print("Cantidad de eventos:", timeline.cantidad_eventos())
print("¿Tiene eventos?:", timeline.tiene_eventos())

print("\nEVENTOS ORDENADOS")

for evento in timeline.obtener_ordenados():
    print(
        evento.fecha.strftime("%d/%m/%Y %H:%M:%S"),
        "-",
        evento.titulo
    )

print("\nDOS EVENTOS MÁS RECIENTES")

for evento in timeline.obtener_recientes(2):
    print(evento.titulo)

print("\nEVENTOS DE CATEGORÍA ACTIVIDAD")

for evento in timeline.obtener_por_categoria("Actividad"):
    print(evento.titulo)

print("\nEVENTOS REGISTRADOS POR FORTUNATO")

for evento in timeline.obtener_por_usuario(
    "Fortunato Tenorio"
):
    print(evento.titulo)