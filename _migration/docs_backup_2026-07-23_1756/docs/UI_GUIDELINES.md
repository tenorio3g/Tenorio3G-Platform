# Tenorio3G Platform
## UI Guidelines

Versión: 1.0  
Estado: En desarrollo  
Área responsable: Product Design / Foundation UI

---

# 1. Propósito

Este documento define los principios, componentes y reglas visuales para construir interfaces dentro de Tenorio3G Platform.

Su objetivo es garantizar que todos los módulos mantengan:

- claridad;
- consistencia;
- facilidad de uso;
- identidad visual;
- capacidad de reutilización;
- adaptación a dispositivos móviles.

Estas reglas aplican a módulos como:

- Work Orders;
- Assets;
- Inventory;
- Tools;
- Purchases;
- People;
- Maintenance;
- Reports;
- Dashboards.

---

# 2. Principios de diseño

## 2.1 Claridad operativa

La información crítica debe mostrarse primero.

El usuario debe poder identificar rápidamente:

- qué elemento está consultando;
- cuál es su estado;
- cuál es su prioridad;
- quién es responsable;
- dónde se encuentra;
- qué acción debe realizar.

---

## 2.2 Menos clics

Las acciones frecuentes deben estar visibles y accesibles.

Ejemplos:

- agregar actividad;
- agregar material;
- asignar técnico;
- cambiar estado;
- editar;
- consultar historial.

Las acciones importantes no deben ocultarse dentro de menús innecesarios.

---

## 2.3 Consistencia

Los componentes deben conservar el mismo comportamiento y apariencia en todos los módulos.

Ejemplos:

- todos los botones principales usan `.btn-primary`;
- todos los estados usan badges;
- todas las métricas usan KPI Cards;
- todos los registros operativos usan Smart Cards o tablas estandarizadas;
- todas las pantallas de detalle comparten una estructura similar.

---

## 2.4 Diseño industrial

Tenorio3G es una plataforma orientada a mantenimiento y operación industrial.

La interfaz debe priorizar:

- lectura rápida;
- datos técnicos claros;
- estados visibles;
- buena separación entre secciones;
- uso cómodo en planta;
- funcionamiento en computadora, tableta y celular.

Los efectos visuales nunca deben dificultar la operación.

---

## 2.5 Reutilización

Antes de crear un nuevo componente se debe verificar si el Foundation UI ya proporciona uno equivalente.

No deben crearse componentes duplicados como:

- `asset-button`;
- `material-button`;
- `tool-button`;
- `purchase-button`.

Todos deben reutilizar el componente base correspondiente.

---

# 3. Jerarquía de una pantalla

Las pantallas de detalle deben seguir esta estructura general:

```text
Página
│
├── Hero Panel
├── Toolbar
├── KPI Section
├── Information Panel
├── Operational Panels
├── Timeline
└── Secondary Information