---
id: 2
title: Create spec for todo CLI app
stage: spec
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-cli-app
branch: 001-todo-cli-app
user: user
command: /sp.specify
labels: [spec, todo-app, cli, python]
links:
  spec: specs/001-todo-cli-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-todo-cli-app/spec.md
 - specs/001-todo-cli-app/checklists/requirements.md
tests:
 - none
---

## Prompt

/sp.specify

Phase I – In-Memory Python Todo Console Application

Target audience:
Beginner to intermediate Python developers and evaluators reviewing agentic, spec-driven development using Claude Code and Spec-Kit Plus.

Focus:
Demonstrate a complete spec-first workflow by building a simple, reliable, in-memory todo CLI application with core CRUD-style functionality and clear user interaction.

Success criteria:
- Implements all 5 basic todo features:
  - Add task
  - View tasks
  - Update task
  - Delete task
  - Mark task complete/incomplete
- Each task includes:
  - Unique ID
  - Title
  - Optional description
  - Completion status
- User can interact entirely through the console
- Invalid input is handled gracefully (no crashes)
- Application behavior directly matches written specifications
- All code is generated via Claude Code (no manual edits)
- Specs are traceable to implementation in the repository

Functional requirements:
- Add Task:
  - User can create a task by providing a title (required)
  - Description is optional
- View Tasks:
  - Displays all tasks in a readable list
  - Shows task ID, title, and completion status
- Update Task:
  - User can modify title and/or description using task ID
- Delete Task:
  - User can remove a task using task ID
- Mark Complete:
  - User can toggle a task's completion status

Constraints:
- Language: Python 3.13+
- Interface: Command-line only
- Storage: In-memory data structures only
- Dependencies: Python standard library only
- Environment: UV-based Python project
- Architecture: Modular, clean, and readable
- Coding standards: PEP 8 compliant

Project structure requirements:
- /src contains all application source code
- /specs-history contains all versions of specifications
- README.md provides setup and run instructions
- CLAUDE.md defines Claude Code usage rules

Timeline:
- Single-phase implementation
- Designed to be completed in one development iteration

Not building:
- File or database persistence
- User authentication or roles
- GUI or web interface
- Advanced task features (priority, due dates, search, filters)
- Testing frameworks or CI/CD setup
- External APIs or services

## Response snapshot

Created comprehensive specification for the In-Memory Python Todo CLI Application. The specification includes:

- 5 user stories covering all required functionality (Add, View, Update, Delete, Mark Complete/Incomplete)
- 10 functional requirements defining system behavior
- 8 measurable success criteria
- Key entity definition for Task
- Edge cases and error handling considerations

The specification follows the template structure and is ready for the planning phase. A quality checklist was also created and validated.

## Outcome

- ✅ Impact: Complete specification created for todo CLI app
- 🧪 Tests: none
- 📁 Files: 2 files created (spec.md, requirements.md)
- 🔁 Next prompts: Plan implementation based on spec
- 🧠 Reflection: Specification covers all required functionality with clear acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin implementation planning