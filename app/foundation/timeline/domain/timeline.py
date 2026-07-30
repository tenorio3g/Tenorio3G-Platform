class Timeline:

    def __init__(self, eventos=None):
        self.eventos = eventos or []

    # =====================================
    # Acciones
    # =====================================

    def agregar_evento(self, evento):
        if evento is None:
            return False

        self.eventos.append(evento)
        return True

    def eliminar_evento(self, evento_id):
        for evento in self.eventos:
            if evento.id == evento_id:
                self.eventos.remove(evento)
                return True

        return False

    # =====================================
    # Consultas
    # =====================================

    def cantidad_eventos(self):
        return len(self.eventos)

    def tiene_eventos(self):
        return len(self.eventos) > 0

    def obtener_ordenados(self, descendente=True):
        return sorted(
            self.eventos,
            key=lambda evento: evento.fecha,
            reverse=descendente
        )

    def obtener_recientes(self, limite=5):
        if limite <= 0:
            return []

        eventos_ordenados = self.obtener_ordenados(
            descendente=True
        )

        return eventos_ordenados[:limite]

    def obtener_por_categoria(self, categoria):
        return [
            evento
            for evento in self.eventos
            if evento.categoria == categoria
        ]

    def obtener_por_usuario(self, usuario):
        return [
            evento
            for evento in self.eventos
            if evento.usuario == usuario
        ]