class OperationsService:

    def resumen(self):
        return {
            "ordenes_abiertas": 12,
            "preventivos_hoy": 3,
            "activos_en_riesgo": 2,
            "tecnicos_trabajando": 5,
            "ordenes_en_espera": 4
        }

    def obtener_metricas(self):
        resumen = self.resumen()

        return [
            {
                "titulo": "Órdenes abiertas",
                "valor": resumen["ordenes_abiertas"],
                "icono": "🔧",
                "descripcion": "Trabajos pendientes",
                "color": "blue"
            },
            {
                "titulo": "Preventivos hoy",
                "valor": resumen["preventivos_hoy"],
                "icono": "🛠",
                "descripcion": "Programados para hoy",
                "color": "orange"
            },
            {
                "titulo": "Activos en riesgo",
                "valor": resumen["activos_en_riesgo"],
                "icono": "⚠️",
                "descripcion": "Requieren atención",
                "color": "red"
            },
            {
                "titulo": "Técnicos trabajando",
                "valor": resumen["tecnicos_trabajando"],
                "icono": "👷",
                "descripcion": "Actualmente asignados",
                "color": "green"
            },
            {
                "titulo": "Órdenes en espera",
                "valor": resumen["ordenes_en_espera"],
                "icono": "⏳",
                "descripcion": "Detenidas temporalmente",
                "color": "yellow"
            }
        ]
    def obtener_ordenes_recientes(self):
        return [
            {
                "numero": "69926",
                "titulo": "Instalación de circuito para TV",
                "estado": "En Proceso",
                "prioridad": "Alta",
                "responsable": "Daniel Hernández"
            },
            {
                "numero": "70001",
                "titulo": "Mantenimiento preventivo de tablero",
                "estado": "Asignada",
                "prioridad": "Media",
                "responsable": "Ángel"
            },
            {
                "numero": "70008",
                "titulo": "Revisión de alumbrado en Ingeniería",
                "estado": "En Espera",
                "prioridad": "Alta",
                "responsable": "Fortunato Tenorio"
            }
        ]
    def obtener_activos_en_riesgo(self):
        return [
            {
                "codigo": "ES09",
                "nombre": "Tablero General ES09",
                "ubicacion": "Subestación Norte",
                "estado": "Operando",
                "salud": 58,
                "riesgo": "Alto"
            },
            {
                "codigo": "COMP-03",
                "nombre": "Compresor 3",
                "ubicacion": "Cuarto de compresores",
                "estado": "En observación",
                "salud": 64,
                "riesgo": "Medio"
            },
            {
                "codigo": "AHU-12",
                "nombre": "Manejadora de aire 12",
                "ubicacion": "Planta alta",
                "estado": "Mantenimiento requerido",
                "salud": 42,
                "riesgo": "Crítico"
            }
        ]
    def obtener_tecnicos(self):
        return [
            {
                "numero": "0001",
                "nombre": "Fortunato Tenorio",
                "rol": "Supervisor",
                "estado": "Coordinando",
                "ordenes_asignadas": 3,
                "carga": 60
            },
            {
                "numero": "0002",
                "nombre": "Daniel Hernández",
                "rol": "Técnico",
                "estado": "Trabajando",
                "ordenes_asignadas": 4,
                "carga": 80
            },
            {
                "numero": "0003",
                "nombre": "Ángel",
                "rol": "Técnico",
                "estado": "Disponible",
                "ordenes_asignadas": 1,
                "carga": 20
            }
        ]