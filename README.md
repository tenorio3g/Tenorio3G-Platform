# 🚀 Tenorio3G Platform

> Transformar la experiencia diaria en conocimiento permanente.

Tenorio3G Platform es una plataforma modular orientada a la gestión de mantenimiento industrial, activos, órdenes de trabajo, personal técnico y conocimiento operativo.

El objetivo es convertir las actividades diarias de mantenimiento en información estructurada, trazable y reutilizable para técnicos, supervisores y responsables de operación.

---

## 📌 Estado actual

**Desarrollo activo**

Tenorio3G ha evolucionado de una base arquitectónica inicial a una plataforma funcional con persistencia, identidad, activos, órdenes de trabajo y un Centro de Operaciones integrado.

### Componentes implementados

| Componente | Estado |
|---|---|
| Foundation | ✅ Operativo |
| Identity / Authentication | ✅ Operativo |
| People | ✅ Operativo |
| Roles / Users | ✅ Operativo |
| Assets | ✅ Operativo |
| Technical Data | ✅ Operativo |
| Spare Parts | ✅ Operativo |
| Documents | ✅ Operativo |
| Work Orders Core | ✅ Operativo |
| Work Order Lifecycle | ✅ Operativo |
| Technician Assignments | ✅ Operativo |
| Work Order Activities | ✅ Operativo |
| Operational Dashboard V2 | ✅ Operativo |
| SQLite Persistence | ✅ Operativo |

---

## 🧪 Calidad y pruebas

La plataforma cuenta actualmente con:

**638 pruebas automatizadas exitosas**

```text
638 passed

Las pruebas cubren progresivamente entidades, repositorios, casos de uso, persistencia y rutas web.

---

## 🆕 Avances recientes

- Centro de Operaciones conectado al flujo de inicio de sesión.
- Dashboard con indicadores obtenidos de datos reales.
- Gestión del ciclo de vida de órdenes de trabajo.
- Asignación y desasignación de técnicos.
- Creación de actividades dentro de órdenes de trabajo.
- Inicio y finalización de actividades.
- Cálculo de avance de actividades.
- Registro de tiempos de ejecución.
- Persistencia de Work Orders en SQLite.
- Persistencia de asignaciones de técnicos.
- Persistencia de actividades.
- Interfaz responsive para escritorio y dispositivos móviles.
- Acceso a la plataforma desde dispositivos de la red local.

---

## 🏗️ Arquitectura

Tenorio3G Platform utiliza una arquitectura modular centrada en dominios:

**Domain-Centered Modular Architecture**

La plataforma busca mantener separadas las responsabilidades mediante:

- Entities
- Value Objects
- Repositories
- Use Cases
- Services
- Presenters
- View Models
- Bootstrap / Dependency Wiring
- Web Routes
- Templates

Esta estructura permite desarrollar cada motor de forma incremental sin acoplar innecesariamente los dominios.

---

## 🧩 Dominios y motores

La plataforma está diseñada para crecer mediante módulos especializados.

Actualmente existen o se encuentran en evolución áreas como:

- Foundation
- Identity
- People
- Assets
- Technical Data
- Spare Parts
- Documents
- Work Orders
- Operations

La arquitectura contempla la incorporación progresiva de otros dominios conforme avance el proyecto.

---

## 🖥️ Centro de Operaciones

Después de autenticarse, el usuario accede al Dashboard principal de Tenorio3G.

Actualmente proporciona acceso e indicadores de:

- Activos
- Órdenes de trabajo
- Personal
- Actividades
- Estado de órdenes
- Operaciones
- Órdenes recientes

El Dashboard funcionará como punto central de navegación conforme se incorporen nuevos motores.

---

## 🔧 Work Orders

El motor de órdenes de trabajo ya permite construir progresivamente el flujo operativo de mantenimiento.

Entre las capacidades actuales se encuentran:

- Crear órdenes.
- Consultar el detalle de una orden.
- Asignar técnicos.
- Quitar técnicos.
- Crear actividades.
- Asignar responsables.
- Iniciar actividades.
- Finalizar actividades.
- Registrar tiempo real.
- Calcular avance.
- Gestionar estados de la orden.

El módulo continuará evolucionando con nuevas capacidades operativas.

---

## 🛠️ Tecnologías

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3
- JavaScript
- Pytest
- Git
- GitHub

---

## 🎯 Visión

Tenorio3G no busca ser únicamente un sistema para registrar órdenes de trabajo.

La visión es construir una plataforma capaz de preservar el conocimiento generado durante la operación:

**Activo → Orden → Actividad → Técnico → Evidencia → Historial → Conocimiento**

De esta manera, una intervención de mantenimiento deja de ser solamente una actividad terminada y se convierte en información reutilizable para futuras decisiones.

---

## 🗺️ Evolución del proyecto

El desarrollo se realiza de forma incremental:

**Foundation → Dominios → Motores → Casos de uso → Persistencia → Web → Integración**

Cada bloque se acompaña de pruebas automatizadas antes de integrarse a la plataforma.

Para el seguimiento detallado del proyecto se mantienen:

- `PROJECT_STATUS.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `docs/architecture/`
- `docs/engines/`

---

## 👤 Autor

**Fortunato Tenorio**

Tenorio3G Platform