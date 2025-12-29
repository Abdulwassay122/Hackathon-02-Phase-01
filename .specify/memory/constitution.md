<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A (new principles added)
Added sections: All principles and sections (initial constitution creation)
Removed sections: N/A
Templates requiring updates: N/A (initial constitution)
Follow-up TODOs: None
-->

# In-Memory Python Todo CLI App Constitution

## Core Principles

### Spec-First Development
No code without a spec; All features must be defined in specification before implementation; Every change traced back to spec requirement

### Agentic Workflow
Strict spec → plan → tasks → implementation workflow; Zero manual coding; Claude Code generates all code following SDD principles

### Clean, Readable Python
Python 3.13+ compliant code; PEP 8 standards; Modular, maintainable code structure; All code must be readable and well-structured

### In-Memory Storage Only
Tasks stored in memory only; No file persistence, no database connections; Console-based interface only; Focus on core functionality first

### Graceful Error Handling
All invalid inputs handled gracefully; Clear error messages for users; No crashes on invalid operations; Defensive programming practices

### Feature Completeness
All 5 mandatory features implemented: Add, View, Update, Delete, Mark Complete/Incomplete; All features fully functional before moving to next phase

## Technology Standards

Python 3.13+ required; Console-based interface only; In-memory storage only; PEP 8 compliant, modular code; Project structure: /src for Python code, /specs-history for spec iterations

## Development Workflow

Spec-driven development: spec → plan → tasks → implementation; Zero manual coding outside Claude Code; All changes must follow SDD principles; Each feature must have traceable specs

## Governance

All code changes must follow spec-driven development; Constitution supersedes all other practices; Amendments require documentation and approval; All PRs must verify compliance with these principles

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29