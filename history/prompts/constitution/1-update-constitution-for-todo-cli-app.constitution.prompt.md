---
id: 1
title: Update constitution for Todo CLI App
stage: constitution
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, todo-app, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Phase I – In-Memory Python Todo CLI App

Objective:
Build a command-line todo application in Python using strict spec-driven, agentic development with Claude Code and Spec-Kit Plus. All tasks are stored in memory.

Core principles:
- Spec-first development (no code without a spec)
- Agentic workflow only (spec → plan → tasks → implementation)
- Zero manual coding (Claude Code generates all code)
- Clean, readable, and maintainable Python

Scope (mandatory features):
- Add task (title required, description optional)
- View all tasks with ID and completion status
- Update task title and/or description
- Delete task by ID
- Mark task complete/incomplete

Standards:
- Python 3.13+
- Console-based interface only
- In-memory storage only (no files, no DB)
- PEP 8 compliant, modular code
- Graceful handling of invalid input

Project structure:
- /src → Python source code
- /specs-history → all spec iterations
- README.md → setup & usage
- CLAUDE.md → Claude Code rules

Success criteria:
- All 5 features implemented and working
- Specs fully traceable to behavior
- App runs without errors
- Repository matches required structure

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with principles for the In-Memory Python Todo CLI App, including: Spec-First Development, Agentic Workflow, Clean, Readable Python, In-Memory Storage Only, Graceful Error Handling, and Feature Completeness. Also defined Technology Standards, Development Workflow, and Governance sections.

## Outcome

- ✅ Impact: Constitution file updated with project-specific principles
- 🧪 Tests: none
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implement the todo app based on the new constitution
- 🧠 Reflection: Constitution now properly defines the development principles for the todo CLI app project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin implementation based on constitution