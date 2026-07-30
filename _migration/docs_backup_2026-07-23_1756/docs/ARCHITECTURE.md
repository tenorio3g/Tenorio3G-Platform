# Tenorio3G Platform

## Filosofía

La plataforma existe para preservar el conocimiento técnico de una empresa.

## El activo es el centro

Toda intervención genera conocimiento.

Toda orden alimenta el historial del activo.

## Principios

1. El conocimiento no debe perderse.
2. Un componente representa un concepto del negocio.
3. Los Services coordinan.
4. Los Models conocen las reglas.
5. Los Repositories manejan la persistencia.

...# Arquitectura de Tenorio3G Platform

## 1. Propósito

Tenorio3G Platform es una plataforma modular orientada a preservar,
organizar y reutilizar el conocimiento técnico generado durante las
operaciones de mantenimiento industrial.

La plataforma debe permitir que activos, órdenes de trabajo, personas,
materiales, herramientas, evidencias y eventos colaboren sin perder
su independencia.

---

## 2. Principio central

> La interfaz solicita, los servicios coordinan, el dominio decide
> y los repositorios administran la persistencia.

---

## 3. Capas de la plataforma

### Presentación

Responsable de mostrar información y recibir acciones del usuario.

Incluye:

- Flask Blueprints
- Routes
- Templates Jinja
- HTML
- CSS
- JavaScript
- Componentes visuales

La presentación no debe contener reglas del negocio.

---

### Aplicación

Responsable de coordinar casos de uso.

Incluye:

- Services
- Casos de uso
- Coordinación entre dominios
- Validación del flujo de aplicación

Ejemplos:

- WorkOrderService
- OperationsService
- EmployeeService

La capa de aplicación coordina, pero no debe sustituir las reglas
internas de los objetos del dominio.

---

### Dominio

Representa los conceptos y reglas reales del negocio.

Incluye entidades como:

- Asset
- AssetEvent
- WorkOrder
- WorkOrderActivity
- WorkOrderMaterial
- WorkOrderTool
- WorkOrderHistory
- WorkOrderEvent
- Employee
- EmployeeRole

El dominio debe poder funcionar y probarse sin Flask.

---

### Infraestructura

Responsable de obtener, guardar y recuperar información.

Incluye:

- Repositories
- Base de datos
- Archivos
- Servicios externos
- APIs
- Integraciones

Actualmente algunos repositorios utilizan datos simulados en memoria.
Más adelante podrán utilizar SQLite y PostgreSQL sin alterar el dominio.

---

### Foundation

Contiene capacidades técnicas compartidas por toda la plataforma.

Capacidades previstas:

- Identity
- Audit
- Events
- Timeline
- Configuration
- Notifications
- Authorization

Foundation no representa un proceso específico de mantenimiento.
Proporciona infraestructura común para los demás módulos.

---

### Shared

Contiene elementos reutilizables que no pertenecen exclusivamente
a un dominio.

Ejemplos:

- Componentes visuales
- Constantes compartidas
- Utilidades generales
- Helpers pequeños
- Design System

Shared no debe convertirse en una carpeta para código sin dueño.

---

## 4. Estructura actual

```text
app/
├── domains/
│   ├── assets/
│   ├── industrial/
│   ├── inventory/
│   ├── knowledge/
│   ├── people/
│   ├── purchases/
│   └── university/
│
├── foundation/
├── operations/
├── shared/
├── static/
├── templates/
├── work_orders/
└── __init__.py