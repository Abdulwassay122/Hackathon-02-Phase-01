---
id: 3
title: repo-consolidation-tasks
stage: tasks
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: repo-consolidation
branch: 3-repo-consolidation
user: user
command: /sp.tasks
labels: [tasks, git, repository, consolidation]
links:
  spec: specs/3-repo-consolidation/spec.md
  plan: specs/3-repo-consolidation/plan.md
  tasks: specs/3-repo-consolidation/tasks.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/3-repo-consolidation/tasks.md
tests:
 - No automated tests for task generation
---

## Prompt

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: $ARGUMENTS

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## User Input

The user provided the context variable `$ARGUMENTS` which refers to the feature specification and plan for Repository Branch Cleanup & Consolidation.

## Response snapshot

---
description: "Task list for Repository Branch Cleanup & Consolidation"
---

# Tasks: Repository Branch Cleanup & Consolidation

**Input**: Design documents from `/specs/3-repo-consolidation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Repository consolidation**: Git operations, file checks, build validation
- Paths shown below are relative to repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository analysis and preparation for consolidation

- [ ] T001 Inspect all branches in repository to understand current state
- [ ] T002 [P] List all files in each branch to identify missing/partial implementations
- [ ] T003 [P] Check build status on each branch to identify working implementations
- [ ] T004 Identify all existing branches that need to be consolidated

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core consolidation infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create backup of repository state before consolidation
- [ ] T006 Switch to main branch and ensure it's up to date
- [ ] T007 [P] Prepare merge strategy for all identified branches
- [ ] T008 Identify all required files that must be preserved from each branch

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Clean Repository State (Priority: P1) 🎯 MVP

**Goal**: Ensure single, clean, working branch with all required files present

**Independent Test**: The repository can be cloned, built successfully, and run without errors or missing files. The main branch contains all necessary code from other branches without conflicts.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Merge 1-fix-db-connection branch into main with conflict resolution
- [ ] T010 [P] [US1] Merge 1-ui-modernization branch into main with conflict resolution
- [ ] T011 [P] [US1] Merge 2-backend-ui-fixes branch into main with conflict resolution
- [ ] T012 [P] [US1] Merge 2-fix-tailwind-css branch into main with conflict resolution
- [ ] T013 [US1] Verify all files from merged branches are present in main
- [ ] T014 [US1] Run build process to ensure main branch compiles successfully
- [ ] T015 [US1] Validate that no broken imports or missing dependencies exist

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Complete Code Coverage (Priority: P1)

**Goal**: Ensure that no valid code from other branches is lost during the consolidation

**Independent Test**: After consolidation, the main branch contains all functionality that was present in any of the other branches without losing essential features.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Compare file listings between original branches and consolidated main
- [ ] T017 [P] [US2] Verify all source code from all branches is present in main branch
- [ ] T018 [US2] Run build process again to confirm all functionality preserved
- [ ] T019 [US2] Validate that no functionality was lost during merge conflicts resolution
- [ ] T020 [US2] Test application functionality to ensure all features work

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Clean Git History (Priority: P2)

**Goal**: Remove or archive unused and broken branches to maintain clean repository structure

**Independent Test**: After consolidation, only the main branch and any necessary long-term branches remain; all temporary and broken branches are removed.

### Implementation for User Story 3

- [ ] T021 [P] [US3] List all branches after consolidation to identify cleanup candidates
- [ ] T022 [US3] Delete unused/consolidated branches (1-fix-db-connection, 1-ui-modernization, 2-backend-ui-fixes, 2-fix-tailwind-css)
- [ ] T023 [US3] Verify only main branch remains with clean commit history
- [ ] T024 [US3] Update README or documentation to reflect new repository structure

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T025 [P] Verify repository builds successfully from clean clone
- [ ] T026 [P] Run any available tests to validate consolidated code
- [ ] T027 [P] Document the consolidation process for future reference
- [ ] T028 Final validation that all requirements from specification are met
- [ ] T029 Final cleanup and repository state validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All implementation tasks for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all merge tasks for User Story 1 together:
Task: "Merge 1-fix-db-connection branch into main with conflict resolution"
Task: "Merge 1-ui-modernization branch into main with conflict resolution"
Task: "Merge 2-backend-ui-fixes branch into main with conflict resolution"
Task: "Merge 2-fix-tailwind-css branch into main with conflict resolution"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Outcome

- ✅ Impact: Created comprehensive task list for repository consolidation
- 🧪 Tests: No automated tests for task generation
- 📁 Files: Created tasks.md with 29 specific tasks organized by user story
- 🔁 Next prompts: Ready for implementation with `/sp.implement` or manual execution
- 🧠 Reflection: Tasks are organized by user story priority with clear dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A for task creation
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task execution