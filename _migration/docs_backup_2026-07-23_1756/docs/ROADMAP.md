# Roadmap — Tenorio3G Platform

## Visión

Tenorio3G Platform busca transformar el trabajo diario de mantenimiento
en conocimiento técnico permanente, estructurado y reutilizable.

La plataforma evolucionará mediante versiones pequeñas y funcionales.
Cada versión deberá incluir:

- Código funcional
- Pruebas
- Documentación
- Revisión arquitectónica
- Criterios de aceptación

---

# Versión 0.1 — Foundation y Activos

## Objetivo

Establecer la arquitectura inicial y crear el expediente técnico de activos.

## Estado

- [x] Application Factory
- [x] Blueprints
- [x] Foundation inicial
- [x] Design System inicial
- [x] Dominio Asset
- [x] AssetEvent
- [x] AssetRepository
- [x] Expediente técnico del activo
- [x] Estado y salud del activo
- [x] Componentes visuales de activos

## Resultado

La plataforma puede representar y mostrar un activo industrial con
información técnica e historial básico.

---

# Versión 0.2 — Órdenes de Trabajo y Personas

## Objetivo

Representar completamente el ciclo operativo de una Orden de Trabajo.

## Estado

### Work Orders

- [x] WorkOrder
- [x] UUID interno
- [x] WorkOrderStatus
- [x] Máquina de estados
- [x] WorkOrderActivity
- [x] WorkOrderMaterial
- [x] WorkOrderTool
- [x] WorkOrderHistory
- [x] WorkOrderEvent
- [x] Porcentaje de avance
- [x] Reglas para asignar, iniciar, finalizar y cerrar
- [x] WorkOrderRepository
- [x] WorkOrderService
- [x] Integración Flask → Service → Repository → Domain
- [x] Vista de detalle de la orden
- [x] Bitácora de eventos

### People

- [x] Employee
- [x] EmployeeRole
- [x] EmployeeRepository
- [x] Supervisor como objeto Employee
- [x] Técnico como objeto Employee
- [x] Requisitor como objeto Employee
- [x] Responsables de actividades como Employee

### Componentes visuales

- [x] Activity Card
- [x] Material Card
- [x] Tool Card
- [x] Technician Card
- [x] Status Badge
- [ ] Timeline Universal
- [ ] Progress Bar compartida
- [ ] Metric Card compartida

### Pendientes de la versión 0.2

- [ ] Evidencias de la orden
- [ ] Comentarios estructurados
- [ ] Pendientes estructurados
- [ ] Timeline Universal
- [ ] Pruebas automatizadas
- [ ] Centro de Operaciones conectado con datos reales
- [ ] Revisión final de arquitectura

## Criterios de aceptación

La versión 0.2 estará terminada cuando:

1. Una orden pueda crearse, asignarse, iniciarse, pausarse, finalizarse y cerrarse.
2. Los cambios importantes queden registrados.
3. La orden tenga solicitante, supervisor y técnicos como objetos Employee.
4. Las actividades calculen el avance automáticamente.
5. El Timeline Universal pueda mostrar eventos de distintos dominios.
6. Las pruebas principales funcionen sin Flask.

---

# Versión 0.3 — Inventario y Compras

## Objetivo

Controlar materiales, refacciones, herramientas y solicitudes de compra.

## Capacidades previstas

### Inventory

- [ ] Catálogo de materiales
- [ ] Catálogo de herramientas
- [ ] Existencias
- [ ] Ubicación de almacén
- [ ] Entradas y salidas
- [ ] Stock mínimo
- [ ] Reservas para órdenes
- [ ] Historial de movimientos

### Purchasing

- [ ] Solicitud de compra
- [ ] Solicitante
- [ ] Equipo o activo relacionado
- [ ] Prioridad
- [ ] Estado de la solicitud
- [ ] Cotización
- [ ] Proveedor
- [ ] Fecha solicitada
- [ ] Fecha recibida
- [ ] Tiempo de espera
- [ ] Entrega al técnico
- [ ] Relación con Orden de Trabajo

### Pizarrón digital

- [ ] Sustituir el pizarrón físico
- [ ] Mostrar solicitudes abiertas
- [ ] Mostrar días transcurridos
- [ ] Alertar solicitudes retrasadas
- [ ] Filtrar por categoría y responsable

---

# Versión 0.4 — Conocimiento Industrial

## Objetivo

Convertir intervenciones y experiencias en conocimiento reutilizable.

## Capacidades previstas

- [ ] Base de conocimiento
- [ ] Lecciones aprendidas
- [ ] Fallas frecuentes
- [ ] Soluciones aplicadas
- [ ] Procedimientos
- [ ] Manuales
- [ ] Diagramas
- [ ] Riesgos conocidos
- [ ] Recomendaciones técnicas
- [ ] Búsqueda por activo, falla o componente

---

# Versión 0.5 — Operaciones y Analítica

## Objetivo

Proporcionar visibilidad operativa y gerencial.

## Capacidades previstas

- [ ] Centro de Operaciones real
- [ ] Órdenes abiertas
- [ ] Preventivos del día
- [ ] Órdenes en espera
- [ ] Activos en riesgo
- [ ] Técnicos trabajando
- [ ] Carga de trabajo
- [ ] Cumplimiento de PM
- [ ] Tiempos promedio
- [ ] Materiales más utilizados
- [ ] Fallas recurrentes
- [ ] Reportes PDF
- [ ] Exportación Excel

---

# Versión 0.6 — Persistencia y Seguridad

## Objetivo

Sustituir repositorios simulados por almacenamiento real y seguro.

## Capacidades previstas

- [ ] SQLite para desarrollo
- [ ] SQLAlchemy
- [ ] Migraciones de base de datos
- [ ] PostgreSQL para producción
- [ ] Usuarios
- [ ] Autenticación
- [ ] Roles y permisos
- [ ] Auditoría
- [ ] Copias de seguridad
- [ ] Recuperación de datos

---

# Versión 0.7 — API y Aplicaciones Móviles

## Objetivo

Permitir que varias interfaces utilicen el mismo núcleo de negocio.

## Capacidades previstas

- [ ] API REST
- [ ] Autenticación de API
- [ ] Aplicación Android
- [ ] Compatibilidad con iPhone
- [ ] Lectura de códigos QR
- [ ] Captura de fotografías
- [ ] Trabajo desde piso de producción
- [ ] Sincronización de información

---

# Versión 0.8 — Asistente Industrial

## Objetivo

Consultar y reutilizar el conocimiento acumulado en la plataforma.

## Capacidades previstas

- [ ] Asistente de mantenimiento
- [ ] Consultas por activo
- [ ] Consultas por falla
- [ ] Historial resumido
- [ ] Recomendaciones basadas en intervenciones anteriores
- [ ] Búsqueda en manuales y procedimientos
- [ ] Alertas predictivas iniciales

---

# Versión 1.0 — Producto Piloto

## Objetivo

Liberar una versión instalable y utilizable en una empresa piloto.

## Criterios generales

- [ ] Multiusuario
- [ ] Gestión de activos
- [ ] Gestión de órdenes
- [ ] Gestión de personas
- [ ] Inventario
- [ ] Compras
- [ ] Conocimiento
- [ ] Dashboard
- [ ] Seguridad
- [ ] Base de datos real
- [ ] API
- [ ] Documentación
- [ ] Instalación reproducible
- [ ] Pruebas principales
- [ ] Primera implementación piloto

---

# Próximo Sprint

## Sprint 0.2.1 — Timeline Universal

### Objetivo

Crear una capacidad compartida para representar cronológicamente eventos
de órdenes, activos, personas, inventario y compras.

### Entregables

- [ ] TimelineEvent
- [ ] Timeline
- [ ] Script de prueba
- [ ] Integración inicial con WorkOrder
- [ ] Componente visual Timeline
- [ ] Documentación arquitectónica
- [ ] Criterios de aceptación cumplidos

### Criterios de aceptación

1. El Timeline debe funcionar sin Flask.
2. Debe aceptar eventos de diferentes categorías.
3. Debe ordenar eventos por fecha.
4. Debe obtener eventos recientes.
5. Debe filtrar por tipo y usuario.
6. WorkOrder podrá utilizarlo sin eliminar todavía su implementación actual.