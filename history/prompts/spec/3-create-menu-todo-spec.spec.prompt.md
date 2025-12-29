---
id: 3
title: Create menu todo spec
stage: spec
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-menu-todo-app
branch: 002-menu-todo-app
user: user
command: /sp.specify
labels: ["specification", "todo-app", "menu-interface"]
links:
  spec: specs/002-menu-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-menu-todo-app/spec.md
 - specs/002-menu-todo-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
Phase I – In-Memory Python Todo CLI App

Target audience:
Developers and reviewers evaluating spec-driven, agentic development with Claude Code.

Focus:
Build a simple, interactive, menu-driven todo CLI application that stores tasks in memory.

CLI flow:
- On start, display a numbered menu
- User selects an option via numeric input
- App prompts for required inputs
- After each action, return to the menu
- App exits only when user selects "Exit"

Menu options:
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit

Success criteria:
- All menu options work as specified
- Tasks have ID, title, optional description, and status
- Clear prompts and messages guide the user
- Invalid input handled gracefully
- All behavior matches the specification
- Code generated only via Claude Code

Constraints:
- Python 3.13+
- Console-only interface
- In-memory storage only
- Standard library only
- PEP 8–compliant, modular code

Not building:
- File/database persistence
- GUI or web interface
- Advanced task features (priority, due dates, search)
```

## Response snapshot

Created comprehensive specification for the interactive menu-driven todo CLI application with 7 user stories covering all menu options, complete with acceptance scenarios, functional requirements (FR-001 to FR-014), key entities, and measurable success criteria (SC-001 to SC-010).

## Outcome

- ✅ Impact: Complete specification created for menu-driven todo app with all required sections
- 🧪 Tests: none
- 📁 Files: specs/002-menu-todo-app/spec.md, specs/002-menu-todo-app/checklists/requirements.md
- 🔁 Next prompts: Ready for planning with /sp.plan
- 🧠 Reflection: Specification follows spec-driven development principles with clear user scenarios

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A