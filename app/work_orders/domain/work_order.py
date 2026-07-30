from datetime import datetime
from uuid import uuid4

from app.foundation.timeline.domain.timeline import Timeline
from app.foundation.timeline.services.timeline_service import TimelineService

from app.work_orders.domain.work_order_status import WorkOrderStatus
from app.work_orders.domain.work_order_history import WorkOrderHistory
from app.work_orders.domain.work_order_event import WorkOrderEvent


class WorkOrder:

    def __init__(
        self,
        numero,
        titulo,
        descripcion,
        tipo,
        prioridad,
        solicitante,
        supervisor,
        activo,
        estado=WorkOrderStatus.CREADA,
        fecha_creacion=None
    ):
        self.id = str(uuid4())

        self.numero = numero
        self.titulo = titulo
        self.descripcion = descripcion
        self.tipo = tipo
        self.prioridad = prioridad
        self.estado = estado

        self.solicitante = solicitante
        self.supervisor = supervisor
        self.activo = activo

        self.fecha_creacion = fecha_creacion or datetime.now()

        self.tecnicos = []
        self.actividades = []
        self.materiales = []
        self.herramientas = []
        self.comentarios = []
        self.pendientes = []
        self.evidencias = []
        self.historial = []
        self.eventos = []

        self.timeline = Timeline()
        self.timeline_service = TimelineService()

    # =====================================
    # Propiedades calculadas
    # =====================================

    @property
    def cantidad_materiales(self):
        """
        Devuelve la cantidad de registros de materiales
        diferentes que tiene la orden.
        """
        return len(self.materiales)

    @property
    def cantidad_total_material(self):
        """
        Devuelve la suma de las cantidades de todos
        los materiales registrados en la orden.
        """
        return sum(
            material.cantidad
            for material in self.materiales
        )

    @property
    def tiene_materiales(self):
        """
        Indica si la orden tiene al menos un material.
        """
        return len(self.materiales) > 0

    @property
    def costo_materiales(self):
        """
        Calcula el costo acumulado de los materiales.
        """
        return sum(
            material.costo_total
            for material in self.materiales
        )

    @property
    def costo_total(self):
        """
        Calcula el costo total de la orden.

        Por ahora solamente incluye materiales.
        Posteriormente podrá incluir mano de obra,
        herramientas y servicios externos.
        """
        return self.costo_materiales

    # =====================================
    # Registro de eventos
    # =====================================

    def _registrar_evento(
        self,
        tipo,
        titulo,
        usuario,
        descripcion=None
    ):
        evento = WorkOrderEvent(
            tipo=tipo,
            titulo=titulo,
            usuario=usuario,
            descripcion=descripcion
        )

        self.eventos.append(evento)

        iconos = {
            "Técnico": "👷",
            "Actividad": "🛠",
            "Material": "📦",
            "Herramienta": "🧰",
            "Estado": "🔄",
            "Comentario": "💬",
            "Evidencia": "📷",
            "Pendiente": "⏳"
        }

        colores = {
            "Técnico": "blue",
            "Actividad": "orange",
            "Material": "purple",
            "Herramienta": "gray",
            "Estado": "green",
            "Comentario": "cyan",
            "Evidencia": "indigo",
            "Pendiente": "yellow"
        }

        self._registrar_evento_timeline(
            categoria=tipo,
            titulo=titulo,
            usuario=usuario,
            descripcion=descripcion,
            icono=iconos.get(tipo, "📄"),
            color=colores.get(tipo, "gray")
        )

        return evento

    def _registrar_evento_timeline(
        self,
        categoria,
        titulo,
        usuario,
        descripcion=None,
        icono="📄",
        color="gray",
        referencia=None
    ):
        return self.timeline_service.registrar_evento(
            timeline=self.timeline,
            categoria=categoria,
            titulo=titulo,
            usuario=usuario,
            descripcion=descripcion,
            icono=icono,
            color=color,
            referencia=referencia or f"OT-{self.numero}"
        )

    # =====================================
    # Métodos privados de materiales
    # =====================================

    def _buscar_material(self, material):
        """
        Busca un material existente.

        Prioridad de búsqueda:
        1. Código del material.
        2. Nombre del material.

        Las comparaciones ignoran mayúsculas,
        minúsculas y espacios exteriores.
        """
        if material is None:
            return None

        codigo_nuevo = (
            material.codigo.strip().lower()
            if material.codigo
            else None
        )

        nombre_nuevo = material.nombre.strip().lower()

        for existente in self.materiales:

            codigo_existente = (
                existente.codigo.strip().lower()
                if existente.codigo
                else None
            )

            nombre_existente = existente.nombre.strip().lower()

            # Cuando ambos tienen código, el código tiene prioridad.
            if codigo_nuevo and codigo_existente:
                if codigo_nuevo == codigo_existente:
                    return existente

                continue

            # Cuando uno o ambos no tienen código,
            # se utiliza el nombre.
            if nombre_nuevo == nombre_existente:
                return existente

        return None

    # =====================================
    # Acciones de la orden
    # =====================================

    def agregar_tecnico(self, tecnico, usuario="Sistema"):
        if tecnico is None:
            return False

        for tecnico_asignado in self.tecnicos:
            if (
                tecnico_asignado.numero_empleado
                == tecnico.numero_empleado
            ):
                return False

        self.tecnicos.append(tecnico)

        nombre_tecnico = getattr(
            tecnico,
            "nombre",
            str(tecnico)
        )

        self._registrar_evento(
            tipo="Técnico",
            titulo="Técnico asignado",
            usuario=usuario,
            descripcion=nombre_tecnico
        )

        return True

    def agregar_actividad(self, actividad, usuario="Sistema"):
        if actividad is None:
            return False

        self.actividades.append(actividad)

        self._registrar_evento(
            tipo="Actividad",
            titulo="Actividad agregada",
            usuario=usuario,
            descripcion=actividad.titulo
        )

        return True

    def agregar_material(self, material, usuario="Sistema"):
        """
        Agrega un material nuevo o aumenta la cantidad
        cuando el material ya existe en la orden.
        """
        if material is None:
            return False

        material_existente = self._buscar_material(material)

        if material_existente is not None:
            cantidad_anterior = material_existente.cantidad

            material_existente.aumentar_cantidad(
                material.cantidad
            )

            cantidad_nueva = material_existente.cantidad

            self._registrar_evento(
                tipo="Material",
                titulo="Cantidad de material actualizada",
                usuario=usuario,
                descripcion=(
                    f"{material_existente.nombre}: "
                    f"{cantidad_anterior} → "
                    f"{cantidad_nueva} "
                    f"{material_existente.unidad}"
                )
            )

            return True

        self.materiales.append(material)

        self._registrar_evento(
            tipo="Material",
            titulo="Material agregado",
            usuario=usuario,
            descripcion=(
                f"{material.nombre}: "
                f"{material.cantidad} "
                f"{material.unidad}"
            )
        )

        return True

    def agregar_herramienta(self, herramienta):
        if herramienta is None:
            return False

        for item in self.herramientas:
            if item.nombre == herramienta.nombre:
                item.cantidad += herramienta.cantidad
                return True

        self.herramientas.append(herramienta)

        return True

    def agregar_comentario(self, comentario):
        if comentario is None:
            return False

        self.comentarios.append(comentario)

        return True

    def agregar_pendiente(self, pendiente):
        if pendiente is None:
            return False

        self.pendientes.append(pendiente)

        return True

    def agregar_evidencia(self, evidencia):
        if evidencia is None:
            return False

        self.evidencias.append(evidencia)

        return True

    # =====================================
    # Estados de la orden
    # =====================================

    def _cambiar_estado(
        self,
        nuevo_estado,
        usuario,
        comentario=None
    ):
        estado_anterior = self.estado
        self.estado = nuevo_estado

        registro = WorkOrderHistory(
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=usuario,
            comentario=comentario
        )

        self.historial.append(registro)

        self._registrar_evento(
            tipo="Estado",
            titulo=f"{estado_anterior} → {nuevo_estado}",
            usuario=usuario,
            descripcion=comentario
        )

        return registro

    def asignar(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.CREADA:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.ASIGNADA,
                usuario,
                comentario
            )
        )

    def iniciar(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.ASIGNADA:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.EN_PROCESO,
                usuario,
                comentario
            )
        )

    def poner_en_espera(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.EN_PROCESO:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.EN_ESPERA,
                usuario,
                comentario
            )
        )

    def reanudar(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.EN_ESPERA:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.EN_PROCESO,
                usuario,
                comentario
            )
        )

    def finalizar(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.EN_PROCESO:
            return False

        if self.porcentaje_avance() < 100:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.FINALIZADA,
                usuario,
                comentario
            )
        )

    def cerrar(self, usuario, comentario=None):
        if self.estado != WorkOrderStatus.FINALIZADA:
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.CERRADA,
                usuario,
                comentario
            )
        )

    def cancelar(self, usuario, comentario=None):
        if self.estado in (
            WorkOrderStatus.FINALIZADA,
            WorkOrderStatus.CERRADA
        ):
            return False

        return bool(
            self._cambiar_estado(
                WorkOrderStatus.CANCELADA,
                usuario,
                comentario
            )
        )

    # =====================================
    # Consultas
    # =====================================

    def tiene_herramientas(self):
        return len(self.herramientas) > 0

    def tiene_pendientes(self):
        return len(self.pendientes) > 0

    def cantidad_tecnicos(self):
        return len(self.tecnicos)

    def cantidad_actividades(self):
        return len(self.actividades)

    def actividades_finalizadas(self):
        return [
            actividad
            for actividad in self.actividades
            if actividad.estado == WorkOrderStatus.FINALIZADA
        ]

    def porcentaje_avance(self):
        if not self.actividades:
            return 0

        total = len(self.actividades)
        finalizadas = len(
            self.actividades_finalizadas()
        )

        return round(
            (finalizadas / total) * 100
        )

    def eventos_timeline(self):
        return self.timeline.obtener_ordenados()

    def cantidad_eventos_timeline(self):
        return self.timeline.cantidad_eventos()