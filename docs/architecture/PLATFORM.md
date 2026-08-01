# TENORIO3G PLATFORM

Versión del documento: 1.0

Estado: En construcción

Autor:
Ingeniero Fortunato Tenorio García

---

# 1. Visión

Tenorio3G Platform es una plataforma modular para la administración del conocimiento técnico, mantenimiento industrial y gestión de activos.

El objetivo no es únicamente registrar información.

El objetivo es preservar el conocimiento técnico de la organización para convertirlo en una ventaja competitiva.

Cada módulo debe contribuir a que el conocimiento permanezca disponible para cualquier persona autorizada, incluso muchos años después de haber sido generado.

---

# 2. Filosofía

Antes de desarrollar funcionalidades se diseña la arquitectura.

Antes de crear pantallas se construye el dominio.

Antes de escribir código se define el modelo de negocio.

La plataforma debe crecer mediante módulos independientes que compartan la misma arquitectura.

Cada módulo debe poder evolucionar sin afectar a los demás.

---

# 3. Objetivos

• Reducir el tiempo necesario para localizar información técnica.

• Conservar el conocimiento adquirido durante los mantenimientos.

• Centralizar la información de los activos.

• Facilitar la toma de decisiones mediante información histórica.

• Servir como base para futuras herramientas de Inteligencia Artificial.

• Convertirse en una plataforma escalable para aplicaciones industriales y universitarias.

---
# 4. Principios de Arquitectura

La arquitectura de Tenorio3G Platform debe proteger el dominio, reducir el acoplamiento y permitir que cada módulo evolucione de forma independiente.

## 4.1 Dependencias dirigidas hacia el dominio

Las capas externas pueden depender de las capas internas.

Las capas internas nunca deben depender de tecnologías de presentación o infraestructura.

Dirección esperada:

```text
Presentation
    ↓
Application
    ↓
Domain
    ↑
Infrastructure

# 5. Capas de la Plataforma

La arquitectura de Tenorio3G Platform está organizada en capas con responsabilidades claramente definidas.

Cada capa conoce únicamente aquello que necesita para cumplir su función.

---

## 5.1 Presentation Layer

Responsabilidad:

Interactuar con el usuario.

Componentes:

- Flask
- HTML
- CSS
- JavaScript
- API REST
- Aplicaciones móviles

Ejemplos:

app/assets/routes.py

templates/

static/

La capa Presentation nunca implementa reglas de negocio.

Su responsabilidad consiste en:

- recibir solicitudes;
- invocar un caso de uso;
- enviar el resultado a un Presenter;
- devolver la respuesta correspondiente.

---

## 5.2 Application Layer

Responsabilidad:

Coordinar la ejecución de una operación del negocio.

Componentes:

- Use Cases
- Commands
- Queries
- Results
- Presenters
- ViewModels

Ejemplo:

GetAssetLifeSheet

Responsabilidades:

- orquestar entidades;
- utilizar repositorios;
- devolver resultados.

No contiene detalles de infraestructura.

---

## 5.3 Domain Layer

Responsabilidad:

Representar el negocio.

Componentes:

- Entities
- Value Objects
- Domain Services
- Policies
- Events

Ejemplo:

Asset

AssetModel

AssetIdentity

AssetLocation

El dominio no conoce:

- Flask;
- HTML;
- SQL;
- HTTP;
- Jinja.

El dominio es independiente de cualquier tecnología.

---

## 5.4 Infrastructure Layer

Responsabilidad:

Implementar servicios técnicos requeridos por el dominio.

Ejemplos:

- Repositorios SQL
- Repositorios InMemory
- PDF
- QR
- Email
- Archivos

La infraestructura implementa contratos definidos por el dominio.

Nunca al contrario.

---

## 5.5 Foundation Layer

Responsabilidad:

Servicios compartidos por toda la plataforma.

Ejemplos:

- Configuración
- Logging
- Auditoría
- Seguridad
- Identity
- Utilidades

Foundation no contiene lógica específica de un módulo.

Debe ser reutilizable por toda la plataforma.

---

## 5.6 Flujo de Dependencias

La dirección permitida de las dependencias es:

Presentation
↓
Application
↓
Domain

Infrastructure
↑

Foundation puede ser utilizada por cualquier capa siempre que no introduzca dependencias circulares.

---

## 5.7 Ejemplo práctico

Solicitud:

Visualizar Hoja de Vida del activo.

Flujo:

Usuario

↓

Flask Route

↓

GetAssetLifeSheet

↓

FindAssetByCode

↓

Repository

↓

Asset

↓

Presenter

↓

ViewModel

↓

HTML

Cada componente participa únicamente dentro de su responsabilidad.

# 6. Estructura Oficial de un Módulo

Todos los módulos de Tenorio3G Platform deberán seguir una estructura uniforme.

El objetivo es que cualquier desarrollador pueda identificar rápidamente dónde se encuentra cada responsabilidad.

La siguiente estructura representa el estándar oficial.

```text
module_name/

├── bootstrap/
│
├── entities/
│
├── value_objects/
│
├── repositories/
│
├── use_cases/
│
├── presenters/
│
├── view_models/
│
├── routes/
│
├── services/
│
├── events/
│
├── exceptions/
│
├── templates/
│
├── static/
│
├── README.md
│
└── __init__.py
```

---

## bootstrap/

Responsabilidad:

Construir el módulo.

Contiene:

- creación de repositorios;
- carga de datos demo;
- registro de casos de uso;
- composición del módulo.

Nunca contiene reglas de negocio.

---

## entities/

Representan conceptos del negocio.

Ejemplos:

Asset

WorkOrder

InventoryItem

Supplier

Las entidades conservan identidad durante todo su ciclo de vida.

---

## value_objects/

Representan conceptos inmutables.

Ejemplos:

AssetIdentity

AssetLocation

Money

Address

Email

Temperature

Los Value Objects se comparan por su contenido.

---

## repositories/

Definen contratos de almacenamiento.

Ejemplos:

AssetRepository

InMemoryAssetRepository

SqlAssetRepository

El dominio depende únicamente del contrato.

---

## use_cases/

Implementan operaciones del negocio.

Cada caso de uso vive en su propia carpeta.

Ejemplo:

```text
register_asset/

    command.py

    result.py

    register_asset.py

    test_register_asset.py

    __init__.py
```

---

## presenters/

Transforman entidades del dominio en objetos preparados para la interfaz.

Nunca contienen reglas del negocio.

---

## view_models/

Representan únicamente la información requerida por la interfaz.

No contienen comportamiento del negocio.

---

## routes/

Punto de entrada HTTP del módulo.

Las rutas únicamente:

- reciben solicitudes;
- invocan casos de uso;
- utilizan Presenters;
- renderizan respuestas.

---

## services/

Servicios propios del módulo que no representan reglas del dominio.

Su utilización debe justificarse claramente.

---

## events/

Eventos del dominio.

Ejemplos:

AssetRegistered

WorkOrderClosed

InventoryAdjusted

---

## exceptions/

Excepciones específicas del módulo.

Ejemplo:

AssetAlreadyExists

InvalidSerialNumber

AssetNotFound

---

## templates/

Plantillas HTML.

Organizadas por funcionalidad.

---

## static/

Archivos estáticos propios del módulo.

CSS

JavaScript

Imágenes

Iconos

---

## README.md

Describe:

- propósito del módulo;
- alcance;
- arquitectura;
- dependencias;
- casos de uso implementados.

---

## __init__.py

Marca el módulo como paquete Python.

No debe contener lógica de negocio.