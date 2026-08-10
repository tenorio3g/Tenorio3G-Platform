# Tenorio3G Platform — Roadmap

## Vision

Tenorio3G Platform aims to become a modular industrial maintenance platform capable of organizing, preserving, analyzing, and using the technical knowledge generated throughout the lifecycle of industrial assets.

The platform evolves incrementally through independent engines built on a common architectural foundation.

The objective is to transform maintenance information into structured technical knowledge that can later support operational analysis and intelligent assistance.

---

# Current Baseline

## v0.6.0

Current stable development baseline.

Completed engines:

- Foundation Engine
- Maps Engine
- Assets Engine
- Technical Data Engine
- Spare Parts Engine
- Documents Engine
- Photos Engine

Automated test suite:

**147 PASSED**  
**0 FAILED**  
**0 ERRORS**  
**0 SKIPPED**

The Photos Engine extends the asset technical record with persistent photographic evidence, physical image storage, image visualization, and primary asset photographs.

---

# Development Roadmap

## Phase 1 — Technical Asset Foundation

**Status: COMPLETE**

This phase established the architectural and technical foundation required to represent industrial equipment and its structured information.

### Foundation Engine

**Status: COMPLETE**

Provides shared infrastructure and architectural foundations.

Main capabilities include:

- Database infrastructure
- SQLAlchemy configuration
- Session management
- Shared metadata
- Common application infrastructure

### Maps Engine

**Status: COMPLETE**

Provides physical asset location and map integration.

### Assets Engine

**Status: COMPLETE**

Provides the central industrial asset model and the foundation for the equipment technical record.

### Technical Data Engine

**Status: COMPLETE**

Provides structured technical specifications associated with industrial assets.

### Spare Parts Engine

**Status: COMPLETE**

Provides spare-parts information and asset relationships.

Capabilities include:

- Spare-part registration
- Asset relationships
- Manufacturer information
- Part numbers
- Installed quantities
- Component positions
- Critical spare-part identification
- Observations
- CRUD operations
- SQLite persistence
- Web integration
- Automated testing

---

# Phase 2 — Technical Knowledge

**Status: COMPLETE**

The objective of this phase is to transform each asset into a digital technical record containing structured information, technical documentation, and visual evidence.

## Documents Engine

**Status: COMPLETE**

Purpose:

Associate real technical documentation with industrial assets.

Implemented capabilities:

- Document domain model
- Asset-document relationships
- Document type classification
- Document metadata
- Repository abstraction
- SQLite persistence
- Create / Read / Update / Delete
- Bootstrap composition
- Presenter
- ViewModel
- Asset-detail integration
- Document registration UI
- Document editing
- Document deletion
- PDF upload
- DocumentStorage abstraction
- LocalDocumentStorage implementation
- Physical PDF storage
- PDF visualization in browser
- Physical file deletion
- PDF file-type validation
- Safe file naming
- HTTP integration tests
- Temporary test storage

Supported document categories include:

- Manuals
- Datasheets
- Electrical diagrams
- Mechanical drawings
- Procedures
- Certifications
- Manufacturer documentation

Uploaded documents are maintained outside Git version control.

The repository preserves the storage directory through:

`storage/documents/.gitkeep`

---

## Photos Engine

**Status: COMPLETE**

Purpose:

Create visual technical evidence and photographic history associated with industrial assets.

Implemented capabilities:

- Photo domain model
- Asset-photo relationships
- Repository abstraction
- SQLite persistence
- Create / Read / Update / Delete
- Bootstrap composition
- Presenter
- ViewModel
- Asset-detail integration
- Photo registration UI
- Photo editing
- Photo deletion
- PhotoStorage abstraction
- LocalPhotoStorage implementation
- Physical JPG / JPEG / PNG storage
- Image visualization
- Photo gallery
- Main asset photograph
- Photo-type classification
- Equipment photographs
- Nameplate photographs
- Component photographs
- Installation evidence
- Maintenance evidence
- Before / after photographs
- Failure evidence
- Inspection evidence
- Photo metadata
- Date tracking
- Physical image deletion
- Image file-type validation
- Safe file naming
- HTTP integration tests
- Temporary test storage
- Storage tests
- Automated primary-photo selection

Uploaded photographs are maintained outside Git version control.

The repository preserves the storage directory through:

`storage/photos/.gitkeep`

User-uploaded image files are excluded through `.gitignore`.

### Primary Photo Rule

Photographs classified with:

`photo_type = "general"`

are candidates to become the main asset photograph.

When multiple general photographs exist, the most recently registered general photograph becomes the primary photograph.

Previous general photographs remain available as historical visual evidence.

The asset technical record now integrates:

Asset  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Documents  
↓  
Photos

---

# Phase 3 — Maintenance Intelligence

**Status: NEXT**

This phase begins using the technical foundation to build a structured operational history for industrial equipment.

## Maintenance History Engine

**Status: NEXT**

Purpose:

Create a complete technical and maintenance history for every asset.

Planned capabilities:

- Maintenance events
- Failures
- Repairs
- Inspections
- Corrective actions
- Technician information
- Materials used
- Spare parts replaced
- Comments
- Technical observations
- Documents
- Photographic evidence
- Event timestamps
- Historical timeline

The objective is to answer questions such as:

- What happened to this equipment?
- When did it fail?
- Who repaired it?
- What component was replaced?
- What materials were used?
- Has this failure happened before?
- What evidence exists from previous interventions?

Maintenance History should integrate information already available from previous engines.

Potential relationship:

Asset  
↓  
Maintenance Event  
├── Spare Parts  
├── Documents  
├── Photos  
├── Technician  
├── Materials  
└── Observations

---

## Preventive Maintenance Engine

**Status: PLANNED**

Purpose:

Manage scheduled and recurring maintenance activities.

Planned capabilities:

- Preventive maintenance plans
- Maintenance frequencies
- Scheduled tasks
- Due dates
- Asset assignments
- Technician assignments
- Completion records
- Alerts
- Overdue maintenance
- Maintenance compliance
- Procedures
- Required spare parts
- Technical documentation references
- Photographic evidence

---

# Phase 4 — Operational Intelligence

**Status: PLANNED**

## Dashboard & Analytics Engine

**Status: PLANNED**

Purpose:

Transform operational and maintenance data into measurable indicators.

Potential KPIs:

- Open work orders
- Completed work orders
- Equipment availability
- Failure frequency
- Preventive maintenance compliance
- Corrective vs preventive maintenance
- Spare-parts usage
- Asset health
- Maintenance workload
- Recurring failures
- Equipment downtime
- Maintenance trends

The objective is to move from recording maintenance activity to understanding operational performance.

---

# Phase 5 — Technical Intelligence

**Status: FUTURE**

## Tenorio AI

**Status: FUTURE**

Purpose:

Create an intelligent technical assistant capable of using the structured information accumulated by Tenorio3G Platform.

Potential capabilities:

- Search technical information
- Analyze maintenance history
- Locate technical documentation
- Locate equipment photographs
- Identify recurring failures
- Suggest troubleshooting steps
- Retrieve spare-part information
- Analyze equipment history
- Compare previous failures
- Assist technicians during diagnostics
- Preserve institutional knowledge
- Provide contextual technical responses

Example:

Technician:

> "Why does AHU-03 keep stopping?"

Tenorio AI could analyze:

Asset  
+  
Technical Data  
+  
Maintenance History  
+  
Spare Parts  
+  
Documents  
+  
Photos  
+  
Work Orders

and provide a contextual technical response based on the accumulated technical history of that equipment.

---

# Architectural Rule

Every new Tenorio3G engine should follow the established development cycle:

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

Storage-oriented engines may additionally include:

Storage Contract  
↓  
Storage Implementation  
↓  
Physical Storage  
↓  
Storage Tests  
↓  
HTTP Integration Tests

before the engine is considered complete.

---

# Development Principles

Tenorio3G development should remain:

- Modular
- Incremental
- Testable
- Maintainable
- Documented
- Reusable
- Scalable

Each engine should have a clear responsibility.

Business logic should remain independent from the user interface whenever possible.

Persistence should remain behind repository abstractions.

Physical file storage should remain behind storage abstractions.

New functionality should include automated tests before being considered complete.

A completed engine should not reduce the stability of previously completed engines.

---

# Release Progression

## v0.4.0

Major milestone:

**Spare Parts Engine completed**

Established the first consolidated architectural baseline.

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts

---

## v0.5.0

Major milestone:

**Documents Engine completed**

Added persistent technical-document management and physical PDF storage.

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts
6. Documents

Automated test suite:

**105 PASSED**

---

## v0.6.0

Major milestone:

**Photos Engine completed**

Added persistent photographic evidence management, physical image storage, image visualization, photo galleries, and primary asset photographs.

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts
6. Documents
7. Photos

Automated test suite:

**147 PASSED**

Next development target:

**Maintenance History Engine**

---

# Long-Term Objective

The long-term objective is not simply to create maintenance software.

The objective is to create a technical knowledge platform where the operational history of an industrial facility becomes a reusable organizational asset.

The expected evolution is:

Maintenance Data  
↓  
Structured Technical Information  
↓  
Technical Evidence  
↓  
Technical Knowledge  
↓  
Maintenance Intelligence  
↓  
Operational Analytics  
↓  
Technical Intelligence

---

# Strategic Direction

Tenorio3G Platform is being built so that every new engine increases the value of the information already stored by previous engines.

An asset should eventually provide access to:

- Identity
- Location
- Technical specifications
- Spare parts
- Documents
- Photographs
- Maintenance history
- Preventive maintenance
- Work orders
- Failure history
- Operational indicators

This accumulated information will form the knowledge base required for future intelligent assistance through Tenorio AI.

---

Tenorio3G Platform

**From maintenance data  
to technical knowledge  
to operational intelligence.**