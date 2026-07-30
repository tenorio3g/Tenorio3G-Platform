from uuid import uuid4

from app.domains.people.domain.employee_role import EmployeeRole


class Employee:

    def __init__(
        self,
        numero_empleado,
        nombre,
        rol=EmployeeRole.TECNICO,
        departamento=None,
        puesto=None,
        turno=None,
        correo=None,
        telefono=None,
        activo=True,
        id=None
    ):
        self.id = id or str(uuid4())

        self.numero_empleado = numero_empleado
        self.nombre = nombre
        self.rol = rol

        self.departamento = departamento
        self.puesto = puesto
        self.turno = turno
        self.correo = correo
        self.telefono = telefono

        self.activo = activo

    # =====================================
    # Consultas
    # =====================================

    def esta_activo(self):
        return self.activo

    def es_tecnico(self):
        return self.rol == EmployeeRole.TECNICO

    def es_supervisor(self):
        return self.rol == EmployeeRole.SUPERVISOR

    def es_requisitor(self):
        return self.rol == EmployeeRole.REQUISITOR

    # =====================================
    # Acciones
    # =====================================

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def cambiar_rol(self, nuevo_rol):
        if nuevo_rol is None:
            return False

        self.rol = nuevo_rol
        return True