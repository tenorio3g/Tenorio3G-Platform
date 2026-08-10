# Tenorio3G Platform — Changelog

All notable changes to Tenorio3G Platform will be documented in this file.

The project follows incremental versioning. Each release represents a stable development milestone validated through automated testing.

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
- Photo metadata
- Asset-photo relationships
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

Supported photographic evidence includes:

- General equipment photographs
- Equipment nameplates
- Component photographs
- Installation evidence
- Maintenance evidence
- Failure evidence
- Inspection evidence
- Before / after photographs

---

### Photo Storage

Added physical file-storage infrastructure for asset photographs.

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

The photo-registration workflow now supports:

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

Supported image formats include:

- JPG
- JPEG
- PNG

Stored file names use the photo code together with a safe version of the original file name.

Example:

`PHOTO-ES09-001__equipment.jpg`

---

### Image Visualization

Added photographic visualization through the application.

Stored photographs can be displayed directly from the asset technical record.

The application connects:

Photo metadata  
↓  
Asset relationship  
↓  
Physical image storage  
↓  
Flask route  
↓  
Browser visualization

Photographs can also be opened individually from the asset interface.

---

### Asset Photo Gallery

Added photographic evidence directly to the asset workspace.

The asset technical record can now display multiple photographs associated with the equipment.

Each photograph can preserve information such as:

- Code
- Title
- Photo type
- File name
- Description
- Registration date

This provides a visual technical-history foundation for future maintenance events.

---

### Primary Asset Photograph

Added automatic primary-photo selection.

Photographs classified as:

`photo_type = "general"`

are candidates for the main asset photograph.

When multiple general photographs exist, the most recently registered general photograph becomes the primary photograph.

Previous general photographs remain stored as historical visual evidence.

This allows the visible representation of an asset to evolve without destroying previous photographs.

---

### Photo Metadata Editing

Added photo metadata editing through the web interface.

Editable information includes:

- Title
- Photo type
- Description

Metadata can be modified without replacing or unnecessarily modifying the physical image file.

---

### Physical Photo Deletion

Photo deletion now removes both:

- SQLite photo metadata
- Associated physical image file

Automated HTTP testing verifies that the database record and physical file are removed correctly.

---

### File Validation

Added image file-type validation to photo uploads.

Unsupported file extensions are rejected before photo metadata is persisted.

Automated tests verify that invalid files:

- Return an HTTP error
- Are not persisted in SQLite
- Are not stored physically

---

## Changed

### Asset Summary

The asset summary can now display the primary equipment photograph.

The previous photographic placeholder has been integrated with the Photos Engine.

When a general photograph exists, the asset summary displays the current primary photograph.

When no general photograph exists, the interface preserves the empty photographic state and provides access to photo registration.

---

### Asset Workspace

The asset workspace now integrates photographic evidence as part of the equipment technical record.

The asset record evolves from:

Asset  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents

to:

Asset  
↓  
Technical Data  
↓  
Spare Parts  
↓  
Technical Documents  
↓  
Photographic Evidence

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
- Create-photo use-case tests
- Get-photo use-case tests
- List-photos-by-asset tests
- Update-photo tests
- Delete-photo tests
- Presenter tests
- Primary-photo selection tests
- Storage tests
- Flask route tests
- HTTP photo creation tests
- Multipart image upload tests
- Image visualization tests
- Invalid-file rejection tests
- Photo metadata editing tests
- Physical image deletion tests

Temporary SQLite databases and temporary filesystem storage are used during HTTP integration testing to isolate automated tests from production data.

---

## Architecture

Photos Engine reuses and extends the storage-oriented architectural pattern established by Documents Engine:

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
Storage Contract  
↓  
Storage Implementation  
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

The successful reuse of this pattern demonstrates that Tenorio3G engines can share architectural principles while maintaining independent domain responsibilities.

---

## Git / Storage

Added Git protection for user-uploaded photographs.

Uploaded images under:

`storage/photos/`

are ignored by Git.

Only:

`storage/photos/.gitkeep`

is version controlled to preserve the required directory structure.

This prevents operational photographs and test images from entering source-control history.

---

## Asset Technical Record

Version 0.6.0 expands the industrial asset technical record with persistent visual evidence.

An asset can now integrate:

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

The asset record can therefore preserve both structured technical information and physical technical evidence.

This establishes the foundation required for future maintenance events to reference photographs, documents, spare parts, and other technical evidence.

---

## Completed Engines

Tenorio3G Platform now has seven completed engines:

1. Foundation Engine
2. Maps Engine
3. Assets Engine
4. Technical Data Engine
5. Spare Parts Engine
6. Documents Engine
7. Photos Engine

---

## Next

The next planned development milestone is:

**Maintenance History Engine**

Its objective is to create a structured historical record of everything that happens to an industrial asset throughout its operational lifecycle.

Planned areas include:

- Maintenance events
- Failures
- Repairs
- Inspections
- Corrective actions
- Technician information
- Materials used
- Spare parts replaced
- Technical observations
- Documents
- Photographic evidence
- Event timestamps
- Historical asset timeline

The Maintenance History Engine will begin connecting information generated by the previously completed engines into a chronological operational record.

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

The document-registration workflow now supports:

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

Technical PDFs can now be opened directly from the asset technical record.

The application verifies:

- Document metadata exists
- Document belongs to the requested asset
- Physical file exists

before returning the PDF to the browser.

---

### Physical Document Deletion

Document deletion now removes both:

- SQLite document metadata
- Associated physical PDF file

The physical file is removed only after the document record has been successfully deleted.

This prevents unnecessary orphaned technical files.

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

New Documents Engine coverage includes:

- Domain tests
- Repository tests
- SQLite repository tests
- Use-case tests
- Presenter tests
- Storage tests
- Flask route tests
- HTTP document creation tests
- Multipart PDF upload tests
- PDF visualization tests
- Physical file deletion tests
- Invalid file rejection tests

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

An asset can now integrate:

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
## v0.6.0

**Photos Engine completed.**

Major additions:

- Photographic-evidence CRUD
- SQLite photo persistence
- JPG / JPEG / PNG upload
- Local photo storage
- Image visualization
- Asset photo gallery
- Primary asset photograph
- Photo metadata editing
- Physical image deletion
- Image file-type validation
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