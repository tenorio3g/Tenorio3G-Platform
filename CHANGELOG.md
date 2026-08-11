# Tenorio3G Platform — Changelog

All notable changes to Tenorio3G Platform will be documented in this file.

The project follows incremental versioning. Each release represents a stable development milestone validated through automated testing.

---

# [0.7.0] — 2026-08-10

## Status

Stable development milestone.

Major milestone:

**Maintenance History Engine completed.**

Automated test suite:

- 184 passed
- 0 failed
- 0 errors
- 0 skipped

---

## Added

### Maintenance History Engine

Added persistent maintenance-history management associated with industrial assets.

The Maintenance History Engine introduces a chronological operational record for each asset and extends the technical record beyond static technical information.

Implemented capabilities include:

- Maintenance event domain model
- Asset-maintenance-event relationships
- Repository abstraction
- In-memory repository
- SQLite persistence
- Create / Read / Update / Delete use cases
- Bootstrap composition
- Presenter
- ViewModel
- Asset-detail integration
- Maintenance registration UI
- Maintenance editing UI
- Maintenance deletion
- Flask route integration
- HTTP integration tests

---

### Maintenance Event Model

Added a dedicated maintenance-event model capable of representing maintenance interventions associated with industrial assets.

Maintenance events can preserve information such as:

- Event code
- Asset code
- Maintenance type
- Title
- Technical description
- Technician / responsible person
- Start timestamp
- Completion timestamp
- Maintenance status
- Technical observations

This creates a structured foundation for preserving the operational history of industrial equipment.

---

### Maintenance Types

Maintenance events can be classified according to their technical purpose.

Current classifications include:

- Corrective maintenance
- Preventive maintenance
- Inspection
- Repair

The architecture can be extended later with additional event classifications without changing the core maintenance-history design.

---

### Maintenance Status

Added maintenance-event status tracking.

Maintenance records can represent interventions that are:

- Open
- Completed

An event without a completion timestamp remains open.

When a completion timestamp is recorded, the maintenance event is presented as completed.

---

### Maintenance Timestamps

Added chronological information to maintenance events.

Maintenance records can preserve:

- Maintenance start date and time
- Maintenance completion date and time

The domain validates that a completion timestamp cannot occur before the event start timestamp.

This provides the foundation for a real operational timeline for each industrial asset.

---

### Technician Information

Added technician / responsible-person information to maintenance records.

Maintenance events preserve who performed or was responsible for the intervention.

This provides traceability and prepares the platform for future integration with personnel, teams, work orders, and technician workload information.

---

### Technical Descriptions and Observations

Maintenance events can preserve both technical descriptions and observations.

The technical description records the intervention or equipment condition associated with the event.

Observations provide additional technical context that may become useful during future diagnostics, recurring-failure analysis, or maintenance planning.

---

### SQLite Persistence

Added persistent SQLite storage for maintenance events.

Maintenance-history information survives application restarts and can be retrieved later as part of the asset lifecycle.

The persistence architecture follows:

Domain  
↓  
Repository Contract  
↓  
SQLite Repository  
↓  
Database Model

The SQLite repository supports:

- Save
- Get by event code
- List by asset code
- Update existing event
- Delete

---

### Maintenance History Use Cases

Added application use cases for maintenance-history management.

Implemented operations include:

- Create maintenance event
- Get maintenance event
- List maintenance events by asset
- Update maintenance event
- Delete maintenance event

These use cases isolate application behavior from Flask routes and persistence infrastructure.

---

### Maintenance History Presentation

Added presentation-layer support for maintenance history.

Introduced:

- Maintenance History Presenter
- Maintenance History ViewModel
- Maintenance event item representation
- Open / completed status presentation
- Formatted timestamps
- Chronological event ordering

Maintenance events are presented with the most recent interventions first.

---

### Asset Maintenance Timeline

Added maintenance history directly to the asset workspace.

An industrial asset can now display a chronological sequence of maintenance events.

The timeline displays information such as:

- Event title
- Event code
- Maintenance type
- Responsible person
- Start timestamp
- Completion timestamp
- Open / completed status
- Technical description
- Observations

This converts the asset record into an increasingly complete operational history.

---

## Changed

### Asset Technical Record

Version 0.7.0 expands the industrial asset technical record with persistent maintenance history.

The asset record evolves from:

Asset  
↓  
Location  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents  
↓  
Photographic Evidence

to:

Asset  
↓  
Location  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents  
↓  
Photographic Evidence  
↓  
Maintenance History

The platform can now preserve not only what an asset is and what technical information belongs to it, but also what has happened to it throughout its operational lifecycle.

---

### Asset Workspace

The asset workspace now integrates maintenance history as part of the equipment technical record.

Technicians can:

- View the maintenance timeline
- Register maintenance events
- Edit maintenance metadata
- Complete open events
- Delete maintenance events

Maintenance-history information is presented chronologically with the most recent interventions first.

---

## Testing

The automated test suite reached:

**184 PASSED**

with:

- 0 FAILED
- 0 ERRORS
- 0 SKIPPED

Maintenance History Engine coverage includes:

- Maintenance-event domain tests
- In-memory repository tests
- SQLite repository tests
- Create-maintenance-event tests
- Get-maintenance-event tests
- List-maintenance-events-by-asset tests
- Update-maintenance-event tests
- Delete-maintenance-event tests
- Bootstrap integration
- Presenter tests
- Chronological ordering tests
- Open / completed status tests
- Flask route tests
- Maintenance-event form tests
- HTTP maintenance creation tests
- Invalid-date rejection tests
- Maintenance editing tests
- Maintenance deletion tests

Temporary SQLite databases are used during integration testing to isolate automated tests from production maintenance data.

---

## Architecture

The Maintenance History Engine follows the established Tenorio3G development pattern:

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
HTTP Integration  
↓  
Tests  
↓  
Git  
↓  
Release

Unlike Documents and Photos, Maintenance History does not require a dedicated physical-file storage layer.

Its primary persistence responsibility is structured maintenance-event information stored through the repository abstraction and SQLite implementation.

---

## Maintenance Knowledge

The completion of Maintenance History establishes an important transition in Tenorio3G Platform.

Previous engines primarily describe the asset:

- What equipment is it?
- Where is it?
- What are its technical characteristics?
- What spare parts does it use?
- What technical documentation belongs to it?
- What does the equipment look like?

Maintenance History adds a new question:

**What has happened to the equipment?**

The platform can now begin preserving operational experience as structured technical knowledge.

---

## Completed Engines

Tenorio3G Platform now has eight completed engines:

1. Foundation Engine
2. Maps Engine
3. Assets Engine
4. Technical Data Engine
5. Spare Parts Engine
6. Documents Engine
7. Photos Engine
8. Maintenance History Engine

---

## Next

The next planned development milestone is:

**Preventive Maintenance Engine**

Its objective is to transform the technical and historical information already associated with industrial assets into structured preventive-maintenance planning.

Planned areas include:

- Preventive maintenance plans
- Maintenance frequencies
- Scheduled maintenance dates
- Recurring maintenance tasks
- Maintenance checklists
- Technician assignments
- Required spare parts
- Required materials
- Required tools
- Technical procedures
- Safety instructions
- Due-date tracking
- Overdue maintenance detection
- Upcoming maintenance identification
- Maintenance completion tracking
- Preventive-maintenance compliance
- Integration with Maintenance History

This moves Tenorio3G Platform from recording what has already happened toward planning what should happen next.

---

# [0.6.0] — 2026-08-09

## Status

Stable development milestone.

Major milestone:

**Photos Engine completed.**

Automated test suite:

- 147 passed
- 0 failed
- 0 errors
- 0 skipped

---

## Added

### Photos Engine

Added complete photographic-evidence management associated with industrial assets.

Implemented capabilities include:

- Photo domain model
- Asset-photo relationships
- Photo metadata
- Photo-type classification
- Repository abstraction
- In-memory repository
- SQLite persistence
- Create / Read / Update / Delete use cases
- Bootstrap composition
- Presenter
- ViewModel
- Asset-detail integration
- Photo registration UI
- Photo editing UI
- Photo deletion
- HTTP integration tests

Supported photographic categories include:

- General equipment photographs
- Nameplate photographs
- Component photographs
- Installation evidence
- Maintenance evidence
- Before photographs
- After photographs
- Failure evidence
- Inspection evidence

---

### Photo Storage

Added physical file-storage infrastructure for technical photographs.

Introduced:

- `PhotoStorage` abstraction
- `LocalPhotoStorage` implementation
- Local photo directory management
- File existence verification
- File-path resolution
- Physical image deletion
- Automated storage tests

Physical photographs are stored under:

`storage/photos/`

The directory structure is preserved in Git through:

`storage/photos/.gitkeep`

User-uploaded image files are excluded from Git version control through `.gitignore`.

---

### Image Upload

Added real image upload support through the Photos web interface.

The photo-registration workflow supports:

Browser  
↓  
Multipart form  
↓  
Flask  
↓  
Image validation  
↓  
Temporary file  
↓  
PhotoStorage  
↓  
Local physical storage  
↓  
SQLite metadata  
↓  
Asset technical record

Supported image extensions include:

- JPG
- JPEG
- PNG

Stored file names use the photo code together with a safe version of the original file name.

---

### Image Visualization

Added image visualization through the application.

Technical photographs can be opened directly from the asset technical record.

The application verifies:

- Photo metadata exists
- Photo belongs to the requested asset
- Physical image exists

before returning the image to the browser.

---

### Physical Photo Deletion

Photo deletion removes both:

- SQLite photo metadata
- Associated physical image file

The physical image is removed only after the photo record has been successfully deleted.

This helps prevent orphaned technical image files.

---

### Image Validation

Added image file-type validation to photo uploads.

Unsupported file extensions are rejected before photo metadata is persisted.

Automated tests verify that invalid files:

- Return an HTTP error
- Are not persisted in SQLite
- Are not stored physically

---

### Photo Metadata Editing

Added photo metadata editing.

Registered photographs can update technical information without requiring the physical image to be replaced.

Editable information includes:

- Title
- Photo type
- Description

This allows photographic evidence to be classified and documented after initial registration.

---

### Main Asset Photograph

Added a primary-photo rule for the asset summary.

Photographs classified as:

`photo_type = "general"`

are candidates to become the main asset photograph.

When multiple general photographs exist, the most recently registered general photograph becomes the primary photograph.

Previous general photographs remain stored as historical visual evidence.

This allows the asset workspace to present a current visual identification of the equipment while preserving previous photographs.

---

### Photo Gallery

Added photographic evidence to the asset workspace.

The asset technical record can display:

- Main equipment photograph
- Photograph title
- Photo classification
- Description
- Registration date
- Additional photographic evidence

This provides visual confirmation of the physical equipment and its technical condition.

---

## Testing

The automated test suite reached:

**147 PASSED**

with:

- 0 FAILED
- 0 ERRORS
- 0 SKIPPED

Photos Engine coverage includes:

- Photo domain tests
- Repository tests
- SQLite repository tests
- Create-photo tests
- Get-photo tests
- List-photos-by-asset tests
- Update-photo tests
- Delete-photo tests
- Presenter tests
- Primary-photo selection tests
- Storage tests
- Flask route tests
- Multipart image upload tests
- Image visualization tests
- Photo metadata editing tests
- Physical image deletion tests
- Invalid-image rejection tests
- HTTP integration tests

Temporary SQLite databases and temporary filesystem storage are used where appropriate to isolate automated tests from production data.

---

## Architecture

The Photos Engine follows the established Tenorio3G development pattern:

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

As a file-oriented engine, Photos additionally follows:

Storage Contract  
↓  
Storage Implementation  
↓  
Physical Storage  
↓  
Storage Tests  
↓  
HTTP Integration

This reuses and validates the storage architecture established by the Documents Engine.

---

## Asset Technical Record

Version 0.6.0 expands the industrial asset technical record with persistent photographic evidence.

An asset can integrate:

Asset  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents  
↓  
Physical PDF Files  
↓  
Photographic Evidence  
↓  
Physical Image Storage

This allows the technical record to preserve both structured information and visual evidence associated with industrial equipment.

---

## Git / Storage

Added Git protection for user-uploaded photographs.

Uploaded images under:

`storage/photos/`

are ignored by Git.

Only:

`storage/photos/.gitkeep`

is version controlled to preserve the required directory structure.

---

## Next

The next planned development milestone is:

**Maintenance History Engine**

Its objective is to associate chronological maintenance events with industrial assets.

Planned areas include:

- Maintenance events
- Corrective maintenance records
- Preventive maintenance records
- Inspections
- Repairs
- Failure interventions
- Technician information
- Maintenance timestamps
- Technical descriptions
- Observations
- Historical asset timeline
- Persistent maintenance-event storage
- Asset-maintenance relationships
- Automated tests

---

# [0.5.0] — 2026-08-09

## Status

Stable development milestone.

Major milestone:

**Documents Engine completed.**

Automated test suite:

- 105 passed
- 0 failed
- 0 errors
- 0 skipped

---

## Added

### Documents Engine

Added complete technical-document management associated with industrial assets.

Implemented capabilities include:

- Document domain model
- Document metadata
- Asset-document relationships
- Document type classification
- Repository abstraction
- In-memory repository
- SQLite persistence
- Create / Read / Update / Delete use cases
- Bootstrap composition
- Presenter
- ViewModel
- Asset-detail integration
- Document registration UI
- Document editing UI
- Document deletion
- HTTP integration tests

Supported technical-document categories include:

- Manuals
- Datasheets
- Electrical diagrams
- Mechanical drawings
- Procedures
- Certifications
- Manufacturer documentation

---

### Document Storage

Added physical file-storage infrastructure for technical documents.

Introduced:

- `DocumentStorage` abstraction
- `LocalDocumentStorage` implementation
- Local document directory management
- File existence verification
- File-path resolution
- Physical file deletion
- Automated storage tests

Physical documents are stored under:

`storage/documents/`

The directory structure is preserved in Git through:

`storage/documents/.gitkeep`

User-uploaded PDF files are excluded from Git version control through `.gitignore`.

---

### PDF Upload

Added real PDF upload support through the Documents web interface.

The document-registration workflow supports:

Browser  
↓  
Multipart form  
↓  
Flask  
↓  
PDF validation  
↓  
Temporary file  
↓  
DocumentStorage  
↓  
Local physical storage  
↓  
SQLite metadata  
↓  
Asset technical record

Stored file names use the document code together with a safe version of the original file name.

Example:

`DOC-ES09-003__manual_es09.pdf`

---

### PDF Visualization

Added secure document visualization through the application.

Technical PDFs can be opened directly from the asset technical record.

The application verifies:

- Document metadata exists
- Document belongs to the requested asset
- Physical file exists

before returning the PDF to the browser.

---

### Physical Document Deletion

Document deletion removes both:

- SQLite document metadata
- Associated physical PDF file

The physical file is removed only after the document record has been successfully deleted.

This helps prevent orphaned technical files.

---

### File Validation

Added PDF file-type validation to document uploads.

Non-PDF file extensions are rejected before document metadata is persisted.

Automated tests verify that invalid files:

- Return an HTTP error
- Are not persisted in SQLite
- Are not stored physically

---

## Testing

The automated test suite reached:

**105 PASSED**

with:

- 0 FAILED
- 0 ERRORS
- 0 SKIPPED

Documents Engine coverage includes:

- Document domain tests
- Repository tests
- SQLite repository tests
- Create-document tests
- Get-document tests
- List-documents-by-asset tests
- Update-document tests
- Delete-document tests
- Presenter tests
- Storage tests
- Flask route tests
- HTTP document creation tests
- Multipart PDF upload tests
- PDF visualization tests
- Physical file deletion tests
- Invalid-file rejection tests

Temporary SQLite databases and temporary filesystem storage are used where appropriate to isolate automated tests from production data.

---

## Architecture

The Documents Engine extends the established Tenorio3G development pattern:

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

File-oriented engines additionally establish the pattern:

Storage Contract  
↓  
Storage Implementation  
↓  
Physical Storage  
↓  
Storage Tests  
↓  
Web Integration

This storage pattern can be reused by future engines such as Photos Engine.

---

## Asset Technical Record

Version 0.5.0 expands the industrial asset technical record.

An asset can integrate:

Asset  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents  
↓  
Physical PDF Files

This moves Tenorio3G Platform closer to its objective of preserving complete industrial technical knowledge around each asset.

---

## Git / Storage

Added Git protection for user-uploaded technical documents.

Uploaded PDFs under:

`storage/documents/`

are ignored by Git.

Only:

`storage/documents/.gitkeep`

is version controlled to preserve the required directory structure.

---

## Next

The next planned development milestone is:

**Photos Engine**

Its objective is to associate visual technical evidence with industrial assets.

Planned areas include:

- Asset photographs
- Equipment nameplates
- Component photographs
- Installation evidence
- Maintenance evidence
- Failure evidence
- Before / after photographs
- Image metadata
- Local image storage
- Asset-photo relationships
- Automated tests

---

# [0.4.0] — 2026-08-07

## Status

Stable development baseline.

Automated test suite:

- 62 passed
- 0 failed
- 0 errors
- 0 skipped

---

## Added

### Foundation Engine

Established the shared architectural foundation used by Tenorio3G Platform.

Provides the base structure required by the platform's modular engines.

---

### Maps Engine

Added map and asset-location capabilities.

Establishes the geographical and physical-location layer for industrial assets.

---

### Assets Engine

Added the central asset domain.

Provides the foundation for representing industrial equipment and associating additional technical information with each asset.

---

### Technical Data Engine

Added structured technical-data management for industrial assets.

Allows technical specifications and equipment information to become part of the asset's digital technical record.

---

### Spare Parts Engine

Added spare-parts management associated with industrial assets.

Provides the architectural foundation for recording and retrieving replacement-part information related to equipment.

---

## Architecture

Consolidated the Tenorio3G engine development pattern:

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

This pattern becomes the reference architecture for future Tenorio3G engines.

---

## Persistence

SQLite persistence is now part of the established engine architecture.

Repository abstractions separate persistence concerns from domain and application logic.

---

## Testing

The automated test suite reached:

**62 PASSED**

with:

- 0 FAILED
- 0 ERRORS
- 0 SKIPPED

This test suite establishes the validation baseline for version 0.4.0.

---

## Documentation

Introduced the formal project documentation structure:

docs/  
├── architecture/  
├── engines/  
└── roadmap/

Added root-level project documentation:

- `PROJECT_STATUS.md`
- `ROADMAP.md`
- `CHANGELOG.md`

---

## Development Process

Established the release workflow:

Tests  
↓  
Commit  
↓  
Tag  
↓  
Changelog  
↓  
Release

Future engines and major milestones should follow this process.

---

## Next

The next planned development milestone begins with:

**Documents Engine**

Its objective is to associate technical documentation with industrial assets, including:

- Manuals
- Datasheets
- Electrical diagrams
- Mechanical drawings
- Procedures
- Certifications
- Manufacturer documentation

---

# Version History

## v0.7.0

**Maintenance History Engine completed.**

Major additions:

- Persistent maintenance events
- SQLite maintenance-history persistence
- Maintenance-event CRUD
- Maintenance type classification
- Technician / responsible-person information
- Start and completion timestamps
- Open / completed maintenance status
- Technical descriptions
- Maintenance observations
- Historical maintenance timeline
- Chronological presentation
- Asset-detail integration
- Maintenance registration UI
- Maintenance editing UI
- Maintenance deletion
- HTTP integration testing

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts
6. Documents
7. Photos
8. Maintenance History

Test baseline:

**184 PASSED**

Next development target:

**Preventive Maintenance Engine**

---

## v0.6.0

**Photos Engine completed.**

Major additions:

- Photo CRUD
- SQLite photo persistence
- Physical image storage
- JPG / JPEG / PNG upload
- Image visualization
- Photo gallery
- Photo metadata editing
- Physical image deletion
- Image validation
- Main asset photograph
- Automated primary-photo selection
- HTTP integration testing

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts
6. Documents
7. Photos

Test baseline:

**147 PASSED**

Next development target:

**Maintenance History Engine**

---

## v0.5.0

**Documents Engine completed.**

Major additions:

- Technical-document CRUD
- SQLite document persistence
- PDF upload
- Local document storage
- PDF visualization
- Physical file deletion
- File-type validation
- HTTP integration testing

Completed engines:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts
6. Documents

Test baseline:

**105 PASSED**

Next development target:

**Photos Engine**

---

## v0.4.0

First consolidated architectural baseline of Tenorio3G Platform.

Completed engine foundation:

1. Foundation
2. Maps
3. Assets
4. Technical Data
5. Spare Parts

Test baseline:

**62 PASSED**

Next development target at the time of release:

**Documents Engine**