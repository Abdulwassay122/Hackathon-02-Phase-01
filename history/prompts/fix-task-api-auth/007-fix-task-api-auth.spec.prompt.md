---
id: "007"
title: "Fix Task API 401 Auth & Migrate DB to Neon PostgreSQL"
stage: "spec"
date_iso: "2026-02-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "fix-task-api-auth"
branch: "007-fix-task-api-auth"
user: "user"
command: "/sp.specify"
labels: ["authentication", "database", "migration", "api", "jwt"]
spec: "specs/007-fix-task-api-auth/spec.md"
ticket: null
adr: null
pr: null
---

# Prompt History Record: Fix Task API 401 Auth & Migrate DB to Neon PostgreSQL

## Files Modified

- specs/007-fix-task-api-auth/spec.md
- specs/007-fix-task-api-auth/checklists/requirements.md

## Tests Run

- None yet (specification phase)

## Prompt Text

```
# Specification: Fix Task API 401 Auth & Migrate DB to Neon PostgreSQL

## Objective
Fix unauthorized (401) responses from the Task API when called from the frontend and Postman using JWT tokens, and migrate the backend database from SQLite to Neon PostgreSQL using an environment-based connection string.

## Problem Statement
- Task API returns 401 even when JWT token is provided
- Token is sent from:
  - Next.js frontend (Authorization header)
  - Postman (Bearer token)
- Backend fails to correctly validate or extract user information
- Backend still uses SQLite despite PostgreSQL URI being present in `.env`

## Scope
- Authentication verification logic
- JWT decoding and user validation
- API request authorization flow
- Database engine configuration

---

## Authentication Fix Requirements

### JWT handling
- Backend must:
  - Read JWT from `Authorization: Bearer <token>` header
  - Verify token signature using shared secret (`BETTER_AUTH_SECRET`)
  - Reject missing or invalid tokens with `401 Unauthorized`
  - Decode token payload to extract:
    - user ID
    - email (if present)

### User enforcement
- Authenticated user ID from JWT must:
  - Match `user_id` in API route parameters
  - Be used to filter all task queries
- Mismatch between token user and route user returns `403 Forbidden`

### API behavior
- All task endpoints require authentication
- Requests without valid JWT return `401`
- Requests with valid JWT but wrong user return `403`
- Successful requests return only the authenticated user's tasks

### Testing
- Verify API access using:
  - Frontend (Next.js)
  - Postman (manual JWT testing)
- Confirm correct HTTP status codes:
  - 200 / 201 → success
  - 401 → missing or invalid token
  - 403 → user mismatch

---

## Database Migration Requirements

### Database engine
- Replace SQLite with Neon PostgreSQL
- Database URL must be read from environment variable:
  - `DATABASE_URL`
- No hardcoded SQLite URLs allowed

### ORM behavior
- SQLModel must:
  - Use PostgreSQL engine
  - Create tables in Neon DB on startup
- Task data must persist across restarts

### Validation
- Confirm:
  - Tables are created in Neon
  - Tasks persist after server restart
  - No SQLite files are created locally

---

## Constraints
- No API contract changes
- No frontend feature changes
- No manual code edits outside Claude Code
- JWT generation remains handled by Better Auth

---

## Success Criteria
- Task API works with valid JWT from frontend and Postman
- 401 errors occur only when expected
- Task ownership is enforced correctly
- Backend uses Neon PostgreSQL exclusively
- Database persistence verified
- Behavior fully matches this specification
```

## Response Text

Created specification file at specs/007-fix-task-api-auth/spec.md with complete requirements for fixing Task API authentication and migrating database to Neon PostgreSQL. The specification includes:

- User scenarios with acceptance criteria
- Functional requirements for JWT handling and user enforcement
- Database migration requirements
- Success criteria with measurable outcomes
- Edge cases consideration

Also created a quality checklist to validate the specification completeness.

## Outcome

Successfully created a comprehensive specification for fixing the Task API 401 authentication issues and migrating the database to Neon PostgreSQL. The specification is ready for the planning phase.

## Evaluation

The specification meets all requirements by defining clear user scenarios, functional requirements for both authentication fixes and database migration, and measurable success criteria. The validation checklist confirms all requirements are properly addressed.