from app.foundation.timeline.domain.timeline_event import TimelineEvent


evento = TimelineEvent(
    categoria="Actividad",
    titulo="Actividad agregada",
    usuario="Fortunato Tenorio",
    descripcion="Preparar área de trabajo",
    icono="🛠",
    color="blue"
)

print("ID:", evento.id)
print("Categoría:", evento.categoria)
print("Título:", evento.titulo)
print("Usuario:", evento.usuario)
print("Descripción:", evento.descripcion)
print("Icono:", evento.icono)
print("Color:", evento.color)
print("Fecha:", evento.fecha)