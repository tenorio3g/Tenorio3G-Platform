from app.domains.people.domain.employee import Employee
from app.domains.people.domain.employee_role import EmployeeRole


class EmployeeRepository:

    def obtener_por_numero(self, numero_empleado):

        numero_empleado = str(numero_empleado).strip()

        if numero_empleado == "0001":
            return Employee(
                numero_empleado="0001",
                nombre="Fortunato Tenorio",
                rol=EmployeeRole.SUPERVISOR,
                departamento="Mantenimiento",
                puesto="Ingeniero de Mantenimiento",
                turno="Primer turno"
            )

        if numero_empleado == "0002":
            return Employee(
                numero_empleado="0002",
                nombre="Daniel Hernández",
                rol=EmployeeRole.TECNICO,
                departamento="Mantenimiento",
                puesto="Técnico de Mantenimiento",
                turno="Primer turno"
            )

        if numero_empleado == "0003":
            return Employee(
                numero_empleado="0003",
                nombre="Ángel",
                rol=EmployeeRole.TECNICO,
                departamento="Mantenimiento",
                puesto="Técnico de Mantenimiento",
                turno="Primer turno"
            )
        
        if numero_empleado == "0004":
            return Employee(
                numero_empleado="0004",
                nombre="Requisitor de Ingeniería",
                rol=EmployeeRole.REQUISITOR,
                departamento="Ingeniería",
                puesto="Ingeniero de Procesos",
                turno="Primer turno"
            )

        return None