from datetime import datetime


class WorkOrderActivity:

    def __init__(
        self,
        titulo,
        descripcion=None,
        responsable=None,
        tiempo_estimado=None
    ):

        self.titulo = titulo
        self.descripcion = descripcion
        self.responsable = responsable

        self.estado = "Pendiente"

        self.tiempo_estimado = tiempo_estimado
        self.tiempo_real = None

        self.fecha_inicio = None
        self.fecha_fin = None

        self.materiales = []
        self.herramientas = []
        self.evidencias = []
        self.comentarios = []


    def iniciar(self):

        self.estado = "En Proceso"
        self.fecha_inicio = datetime.now()
    
    def finalizar(self):

        self.estado = "Finalizada"
        self.fecha_fin = datetime.now()

        if self.fecha_inicio:

            diferencia = self.fecha_fin - self.fecha_inicio

            self.tiempo_real = diferencia
    