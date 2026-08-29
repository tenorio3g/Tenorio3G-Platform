# Tenorio3G Platform ? Engines

## Purpose

This document provides a high-level view of the modular engines currently implemented in Tenorio3G Platform.

An engine exists because it owns a meaningful responsibility.

It should not exist merely to create another folder or abstraction.

---

# Current Architecture

Tenorio3G is no longer exclusively asset-centered.

The platform currently has two major functional branches built on a shared foundation:

Foundation
|
+-- Asset Knowledge
|   +-- Maps
|   +-- Assets
|   +-- Technical Data
|   +-- Spare Parts
|   +-- Documents
|   +-- Photos
|   +-- Maintenance History
|   +-- Preventive Maintenance
|
+-- Operational Maintenance
    +-- Work Orders
    +-- Work Sessions

Cross-cutting capabilities include identity, authorization, persistence, testing, source-quality controls, and web integration.

Future analytical capabilities will consume information from both branches.

---

# 1. Foundation Engine

## Status

**COMPLETE**

## Responsibility

Provide shared architectural and infrastructure capabilities required by the rest of the platform.

Foundation should not contain engine-specific business behavior.

Primary responsibilities include:

- Database configuration
- SQLAlchemy infrastructure
- Session management
- Shared metadata
- Application composition
- Shared services

---

# 2. Maps Engine

## Status

**COMPLETE**

## Responsibility

Provide physical-location context for industrial assets.

Maps helps answer:

- Where is the equipment?
- In which area is it located?
- How can a technician find it?

---

# 3. Assets Engine

## Status

**COMPLETE**

## Responsibility

Represent industrial assets as persistent central entities.

Assets provide the digital identity of physical equipment and serve as an integration point for technical information.

---

# 4. Technical Data Engine

## Status

**COMPLETE**

## Responsibility

Store structured equipment specifications and technical information.

Examples include:

- Manufacturer
- Model
- Serial number
- Voltage
- Current
- Power
- Capacity
- Frequency
- Equipment-specific ratings

---

# 5. Spare Parts Engine

## Status

**COMPLETE**

## Responsibility

Manage replacement-part information associated with industrial assets.

Capabilities include:

- Part registration
- Manufacturer
- Part number
- Quantity
- Unit
- Position
- Critical-part identification
- Observations
- Asset relationships
- SQLite persistence
- CRUD
- Web integration

Milestone:

**v0.4.0**

---

# 6. Documents Engine

## Status

**COMPLETE**

## Responsibility

Manage technical documentation associated with industrial assets.

Capabilities include:

- Document metadata
- Asset relationships
- SQLite persistence
- CRUD
- PDF upload
- Local document storage
- PDF visualization
- Physical deletion
- File validation
- Safe file naming
- HTTP integration

Milestone:

**v0.5.0**

---

# 7. Photos Engine

## Status

**COMPLETE**

## Responsibility

Manage photographic technical evidence.

Capabilities include:

- Photo metadata
- Asset relationships
- SQLite persistence
- CRUD
- JPG / JPEG / PNG storage
- Photo visualization
- Photo gallery
- Primary asset photograph
- Photo classification
- Maintenance evidence
- Failure evidence
- Installation evidence
- Inspection evidence
- Physical deletion
- Image validation

Milestone:

**v0.6.0**

---

# 8. Maintenance History Engine

## Status

**COMPLETE**

## Responsibility

Preserve chronological maintenance history for industrial assets.

Capabilities include:

- Maintenance event domain model
- Asset relationships
- SQLite persistence
- CRUD
- Maintenance classifications
- Technician information
- Start and completion timestamps
- Open / completed status
- Technical descriptions
- Observations
- Historical timeline
- Web integration

Milestone:

**v0.7.0**

Historical implementation commit:

`3b37780`

---

# 9. Preventive Maintenance Engine

## Status

**COMPLETE**

## Responsibility

Manage preventive-maintenance planning and execution.

Capabilities include:

- Preventive maintenance plans
- Preventive maintenance executions
- Plan creation
- Plan retrieval
- Plan update
- Plan deletion
- Plan completion
- Execution history
- In-memory repositories
- SQLite repositories
- Presenters
- ViewModels
- Metrics
- Bootstrap composition
- Web integration
- Automated testing

Milestone:

**v0.8.0**

Historical implementation commit:

`7b75037`

---

# 10. Work Orders Engine

## Status

**COMPLETE**

## Responsibility

Manage operational maintenance work from request through execution.

Capabilities include:

- Flexible requests
- Requester information
- Work-order lifecycle
- Approval workflow
- Assignment workflow
- Supervisor information
- Technician assignments
- Activities
- Activity lifecycle
- Spare-part consumption
- Tool issue and return
- Evidence
- Persistent lifecycle timeline
- Technician history
- Operational dashboards
- SQLite persistence
- Flask integration
- Automated testing

Important lifecycle rule:

A work order must be approved before it can be assigned.

Conceptual lifecycle:

Created<br>
?<br>
Approved<br>
?<br>
Assigned<br>
?<br>
In Progress

Additional completion and cancellation behavior remains governed by domain rules.

---

# 11. Work Sessions Engine

## Status

**COMPLETE**

## Responsibility

Record actual work periods performed by technicians against work-order activities.

Capabilities include:

- Automatic sessions
- Manual sessions
- Start
- End
- Manual creation
- Manual correction
- Person validation
- Actor validation
- Ownership validation
- Active-session protection
- Overlap detection
- Duration calculation
- In-memory repository
- SQLite repository
- Audit repository
- Manual-created audit events
- Correction audit events
- Bootstrap composition
- SQLite integration testing

Overlap behavior uses half-open time intervals.

For example:

08:00?10:00<br>
10:00?11:00

does not represent an overlap.

Normal session termination requires the actor to own that work session.

Administrative correction is a separate workflow.

---

# Operational Maintenance Relationship

Work Order
|
+-- Request
+-- Approval
+-- Assignment
+-- Supervisor
+-- Technicians
+-- Activities
+-- Spare Parts
+-- Tools
+-- Evidence
+-- Timeline
+-- Work Sessions
    +-- Automatic
    +-- Manual
    +-- Corrections
    +-- Overlap Control
    +-- Audit

Work Sessions belong to the operational execution layer rather than the asset technical-record layer.

---

# Current Platform Baseline

Candidate version:

**v0.9.0**

Current implementation commit:

`455572b`

Current automated regression:

**1925 PASSED**

Work Sessions suite:

**132 PASSED**

The total regression count includes repository-wide source-encoding validation.

---

# Quality Controls

Active project source uses:

**UTF-8 without BOM**

Repository controls include:

- `.editorconfig`
- `.gitattributes`
- Source encoding tests
- BOM detection
- Invalid UTF-8 detection
- Mojibake detection

---

# Release Progression

v0.4.0<br>
Spare Parts<br>
?<br>
v0.5.0<br>
Documents<br>
?<br>
v0.6.0<br>
Photos<br>
?<br>
v0.7.0<br>
Maintenance History<br>
?<br>
v0.8.0<br>
Preventive Maintenance<br>
?<br>
v0.9.0<br>
Operational Maintenance<br>
Work Orders + Work Sessions

---

# Next Architectural Stage

## Operational Intelligence

**Status: NEXT**

Purpose:

Convert operational maintenance information into reliable performance indicators.

Potential areas include:

- Work-order KPIs
- Preventive maintenance compliance
- Technician workload
- Work-session analysis
- Downtime
- Failure frequency
- Maintenance backlog
- Spare-part consumption
- Asset reliability
- Operational trends

Existing dashboard work should be consolidated into this analytical layer.

---

# Future Stage

## Tenorio AI

**Status: FUTURE**

Tenorio AI should operate on structured platform information rather than isolated prompts.

Potential context includes:

- Assets
- Technical Data
- Spare Parts
- Documents
- Photos
- Maintenance History
- Preventive Maintenance
- Work Orders
- Work Sessions
- Operational Analytics

---

# Engine Design Principle

Every engine should answer:

1. What information does it own?
2. What behavior does it provide?
3. Which other concepts does it reference?
4. What should remain outside its responsibility?

Business logic should remain independent from the user interface whenever practical.

Persistence should remain behind repository abstractions.

Physical storage should remain behind storage abstractions.

New functionality should include automated tests before being considered complete.

A completed engine should not reduce the stability of previously completed engines.

---

Tenorio3G Platform

**From maintenance data<br>
to technical knowledge<br>
to operational intelligence.**
