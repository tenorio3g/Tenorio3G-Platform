from app.domains.people.domain.employee import Employee
from app.domains.people.domain.employee_role import EmployeeRole


empleado = Employee(
    numero_empleado="0001",
    nombre="Fortunato Tenorio",
    rol=EmployeeRole.SUPERVISOR,
    departamento="Mantenimiento",
    puesto="Ingeniero de Mantenimiento",
    turno="Primer turno"
)

print("ID interno:", empleado.id)
print("Número:", empleado.numero_empleado)
print("Nombre:", empleado.nombre)
print("Rol:", empleado.rol)
print("Departamento:", empleado.departamento)
print("Puesto:", empleado.puesto)
print("Turno:", empleado.turno)
print("Activo:", empleado.esta_activo())
print("¿Es técnico?:", empleado.es_tecnico())
print("¿Es supervisor?:", empleado.es_supervisor())

empleado.desactivar()

print("Activo después de desactivar:", empleado.esta_activo())
print(type(empleado))