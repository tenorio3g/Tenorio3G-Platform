# Tenorio3G Platform — Documentación oficial

> Preservar el conocimiento técnico, facilitar el trabajo y evolucionar continuamente.

---

## Propósito

Esta carpeta contiene la documentación oficial de Tenorio3G Platform.

Su objetivo es explicar:

- por qué existe el proyecto;
- cómo está organizado;
- qué principios gobiernan su desarrollo;
- cómo funciona su arquitectura;
- cómo deben construirse sus módulos;
- cuál es su estado actual;
- hacia dónde evolucionará.

La documentación forma parte del producto y debe mantenerse junto con el código.

---

## ¿Qué es Tenorio3G Platform?

Tenorio3G Platform es una plataforma modular orientada a la gestión del mantenimiento industrial, los activos, las órdenes de trabajo, el conocimiento técnico y los procesos operativos.

Su propósito principal es convertir la experiencia acumulada de una organización en información estructurada, verificable, accesible y reutilizable.

Tenorio3G no pretende limitarse a registrar actividades.

Busca conservar la historia técnica de los activos, facilitar la continuidad operativa y reducir la dependencia de la memoria individual.

---

## Organización documental

### 00 — Foundation

Contiene la identidad y los fundamentos del proyecto.

Documentos principales:

- `PROJECT_CHARTER.md`
- `VISION.md`
- `MANIFESTO.md`
- `CONSTITUTION.md`
- `GLOSSARY.md`

### 01 — Architecture

Describe la estructura técnica de la plataforma, sus capas, dependencias, módulos y decisiones arquitectónicas.

Documentos principales:

- `ARCHITECTURE.md`
- `ADR/`

### 02 — Engineering

Define la metodología y los estándares utilizados para construir Tenorio3G.

Documentos principales:

- `TEF.md`
- estándares de programación;
- estándares de componentes;
- estrategia de pruebas;
- proceso de liberación.

### 03 — Project

Contiene la información operativa y evolutiva del proyecto.

Documentos principales:

- `ROADMAP.md`
- `CHANGELOG.md`
- `PROJECT_STATUS.md`
- `BACKLOG.md`

### 04 — Product

Contiene la documentación funcional de los módulos de negocio.

Ejemplos:

- Assets
- Work Orders
- Knowledge
- Inventory
- Users
- Dashboard

---

## Orden recomendado de lectura

Una persona que ingrese por primera vez al proyecto deberá leer los documentos en este orden:

1. `00_foundation/PROJECT_CHARTER.md`
2. `00_foundation/VISION.md`
3. `00_foundation/MANIFESTO.md`
4. `00_foundation/CONSTITUTION.md`
5. `00_foundation/GLOSSARY.md`
6. `01_architecture/ARCHITECTURE.md`
7. `02_engineering/TEF.md`
8. `03_project/PROJECT_STATUS.md`
9. `03_project/ROADMAP.md`
10. Documentación del módulo correspondiente en `04_product/`

---

## Principios documentales

Toda documentación de Tenorio3G deberá cumplir las siguientes reglas:

1. Tener un propósito claro.
2. Mantenerse en una ubicación coherente.
3. Evitar duplicar información.
4. Registrar decisiones importantes.
5. Mantener relación con el código implementado.
6. Actualizarse cuando cambie el comportamiento del sistema.
7. Utilizar lenguaje claro, técnico y verificable.

---

## Regla de las tres preguntas

Antes de crear cualquier archivo, se deberá responder:

1. ¿Por qué existe?
2. ¿Dónde debe vivir?
3. ¿Quién dependerá de él?

Si estas preguntas no pueden responderse claramente, el archivo todavía no debe crearse.

---

## Estado del proyecto

| Campo | Valor |
|---|---|
| Proyecto | Tenorio3G Platform |
| Versión | `0.1.0-alpha` |
| Fase | Foundation |
| Sprint | `FND-010` |
| Estado | En desarrollo |
| Product Owner | Ing. Fortunato Tenorio García |

---

## Responsabilidad de mantenimiento

La documentación deberá revisarse cuando ocurra alguno de estos eventos:

- creación de un módulo;
- cambio arquitectónico;
- incorporación de una dependencia relevante;
- modificación de un proceso;
- publicación de una versión;
- aceptación de una decisión mediante ADR;
- cambio de alcance o prioridad.

---

## Autoría

**Proyecto:** Tenorio3G Platform  
**Fundador y Product Owner:** Ing. Fortunato Tenorio García  
**Arquitectura y acompañamiento técnico:** ChatGPT  