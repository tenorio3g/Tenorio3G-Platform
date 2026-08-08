# Tenorio3G Platform — Engine Architecture

## Purpose

This document defines the reference architecture used to develop modular engines inside Tenorio3G Platform.

Its purpose is to maintain consistency as the platform grows and to prevent business logic, persistence, presentation, and user-interface responsibilities from becoming coupled.

Every new engine should follow this architecture unless there is a documented technical reason to deviate from it.

---

# Reference Development Flow

Each Tenorio3G engine follows this development cycle:

Idea
↓
Domain
↓
Repository
↓
SQLite
↓
Use Cases
↓
Bootstrap
↓
Presenter
↓
ViewModel
↓
UI
↓
Tests
↓
Git
↓
Release

The arrows represent the development sequence.

They do not mean that every layer should directly depend on the next one.

Dependencies should remain controlled and responsibilities separated.

---

# 1. Idea

Before writing code, define the responsibility of the engine.

Questions to answer:

- What problem does this engine solve?
- What information does it manage?
- What operations must it support?
- Which existing engine does it depend on?
- What should NOT be the responsibility of this engine?

Example:

Documents Engine manages technical-document metadata and its relationship with industrial assets.

It should not contain maintenance-history logic.

---

# 2. Domain

The Domain represents the business concepts of the engine.

Examples:

Asset

TechnicalData

SparePart

Document

Domain objects should describe what the system manages without depending on Flask, HTML, HTTP routes, or database-specific implementation details.

Typical responsibilities:

- Business entities
- Value objects
- Business rules
- Domain validation
- Domain behavior

The domain should remain as independent as reasonably possible from infrastructure and presentation concerns.

---

# 3. Repository

Repositories define how the application accesses stored information.

The application should work with repository abstractions instead of embedding SQL operations throughout business logic.

Conceptually:

Use Case
    ↓
Repository
    ↓
Persistence

Typical repository operations may include:

- add
- get
- list
- update
- delete

The exact interface depends on the engine.

Repositories help isolate persistence concerns from domain and application logic.

---

# 4. SQLite Persistence

SQLite is the current persistence technology used by Tenorio3G Platform.

Database-specific responsibilities belong in the infrastructure/persistence implementation rather than in domain objects.

Typical responsibilities:

- Tables
- SQL statements
- Row mapping
- Connections
- Transactions
- Persistence implementation

Conceptually:

Domain / Application
        │
        ▼
Repository abstraction
        │
        ▼
SQLite implementation
        │
        ▼
Database

This separation makes future persistence changes easier to manage.

---

# 5. Use Cases

Use Cases represent application operations.

They coordinate domain objects and repositories to accomplish a specific action.

Examples:

Create asset

Add technical data

Register spare part

Update document

Delete document

A use case should have a clear responsibility.

Instead of placing application logic directly inside Flask routes:

Route
    ↓
Business logic
    ↓
SQL

Tenorio3G should prefer:

Route
    ↓
Use Case
    ↓
Repository
    ↓
Persistence

This keeps HTTP concerns separate from application behavior.

---

# 6. Bootstrap

Bootstrap is responsible for composing dependencies.

It connects concrete infrastructure implementations with application components.

Examples:

SQLite repository
        ↓
Use Case
        ↓
Presenter / Route

Bootstrap prevents every route from manually constructing the dependency graph.

Its responsibility is composition, not business logic.

---

# 7. Presenter

The Presenter transforms application results into information suitable for presentation.

It should not contain persistence logic.

Typical responsibilities:

- Transform application output
- Prepare presentation-oriented structures
- Normalize display information
- Build ViewModels

Conceptually:

Use Case Result
      ↓
Presenter
      ↓
ViewModel

---

# 8. ViewModel

A ViewModel represents the data required by a specific user interface.

The UI should not need to understand domain internals or database structures.

Example:

Asset domain object

may contain business-oriented information.

The corresponding AssetViewModel may contain:

- Display name
- Status label
- Location text
- Health indicator
- Action availability
- Formatted dates

ViewModels are presentation-oriented structures.

---

# 9. UI

The UI is responsible for interaction and visualization.

In the current Tenorio3G web application this may include:

- Flask routes
- Jinja templates
- HTML
- CSS
- JavaScript
- Forms

The UI should coordinate requests and responses but avoid becoming the location for business rules or SQL queries.

Preferred flow:

HTTP Request
      ↓
Route
      ↓
Use Case
      ↓
Repository
      ↓
Persistence
      ↓
Result
      ↓
Presenter
      ↓
ViewModel
      ↓
Template
      ↓
HTTP Response

---

# 10. Tests

An engine is not considered complete only because its interface works visually.

Its behavior should be validated through automated tests.

Tests may cover:

- Domain behavior
- Repository behavior
- Persistence
- Use cases
- Presenters
- ViewModels
- Routes
- Integration behavior

Before a release:

pytest

should complete without failures.

The current v0.4.0 baseline is:

62 passed
0 failed
0 errors
0 skipped

Future development must preserve previously validated behavior unless an intentional change is documented.

---

# 11. Git

Stable development milestones should be recorded using Git.

Recommended workflow:

Implement
↓
Test
↓
Review
↓
Document
↓
Commit

Commit messages should describe the technical change clearly.

Avoid combining unrelated changes into a single commit when practical.

---

# 12. Release

A release represents a known state of Tenorio3G Platform.

Before creating a release:

- Relevant functionality is complete
- Tests pass
- Documentation is updated
- CHANGELOG.md is updated
- Git working state is reviewed
- Version number is defined

The release can then be identified using a Git tag.

Example:

v0.4.0

---

# Dependency Direction

One of the most important architectural principles is dependency control.

Higher-level business concepts should not become unnecessarily dependent on lower-level implementation details.

Preferred conceptual direction:

UI
↓
Application / Use Cases
↓
Domain

Infrastructure provides implementations required by the application.

For example:

Application
      │
      ▼
Repository abstraction
      ▲
      │
SQLite repository implementation

The application depends on the repository contract.

Infrastructure implements that contract.

This reduces coupling between business behavior and persistence technology.

---

# Engine Independence

Each engine should have one clearly defined responsibility.

Examples:

Assets Engine
    → asset identity and lifecycle

Technical Data Engine
    → technical specifications

Spare Parts Engine
    → replacement-part information

Documents Engine
    → technical documentation

Photos Engine
    → photographic evidence

Maintenance History Engine
    → maintenance events and historical records

Preventive Engine
    → scheduled maintenance

Engines may collaborate, but their responsibilities should not become mixed.

---

# Asset-Centered Architecture

The industrial asset is one of the central concepts of Tenorio3G.

Future engines can progressively enrich the asset's technical record:

Asset
│
├── Location / Maps
│
├── Technical Data
│
├── Spare Parts
│
├── Documents
│
├── Photos
│
├── Maintenance History
│
└── Preventive Maintenance

This creates a progressively richer digital technical record for each piece of industrial equipment.

---

# Architectural Rules

## Rule 1

Do not place SQL directly inside templates.

## Rule 2

Avoid placing business rules directly inside Flask routes.

## Rule 3

Domain objects should not depend on HTML or templates.

## Rule 4

Persistence details should remain behind repository implementations.

## Rule 5

Use Cases should represent clear application actions.

## Rule 6

Presenters and ViewModels should prepare information for the UI without becoming persistence layers.

## Rule 7

New engines should include automated tests.

## Rule 8

Existing tests must continue passing unless a deliberate behavioral change requires updating them.

## Rule 9

Each file should have a clear purpose.

## Rule 10

Prefer small, incremental changes over large unverified modifications.

---

# Definition of Done — Engine

A Tenorio3G engine can be considered complete when its required layers are implemented and validated.

Depending on the engine, this may include:

- Domain
- Repository abstraction
- Persistence implementation
- Use Cases
- Bootstrap
- Presenter
- ViewModels
- Routes
- Templates
- Automated tests
- Documentation

Not every engine must have identical files.

The architecture defines responsibilities, not unnecessary boilerplate.

---

# Guiding Principle

Tenorio3G should grow through reusable architectural patterns rather than isolated features.

The objective is not simply to make functionality work.

The objective is to make functionality understandable, testable, maintainable, and capable of evolving without destabilizing the rest of the platform.