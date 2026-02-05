# Implementation Plan: Fix 401 Unauthorized Error on Dashboard

**Branch**: `001-fix-dashboard-auth` | **Date**: 2026-02-03 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-fix-dashboard-auth/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of authentication fixes for the dashboard route to resolve 401 Unauthorized errors. This involves adding frontend route protection to redirect unauthenticated users to login, implementing proper token validation, and ensuring consistent authentication state across page refreshes while maintaining existing backend authentication middleware.

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript/Next.js (frontend)
**Primary Dependencies**: FastAPI (backend), Next.js 16+ (frontend), SQLModel, python-jose
**Storage**: SQLite database via SQLModel
**Testing**: pytest for backend, Jest/React Testing Library for frontend (planned)
**Target Platform**: Web application (Linux/Mac/Windows compatible)
**Project Type**: Web application (full-stack)
**Performance Goals**: <200ms p95 for auth validation, <1s page load for dashboard
**Constraints**: <100MB memory usage, maintain existing API contracts, no breaking changes
**Scale/Scope**: Single tenant application, up to 10k users

### Current Architecture
- **Backend**: FastAPI application with JWT-based authentication middleware
- **Frontend**: Next.js app router with client-side authentication state management
- **Authentication Flow**: Login → JWT token → API calls with Authorization header
- **Route Protection**: Backend API endpoints protected via middleware, frontend routes currently unprotected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principles Alignment
- ✅ **Spec-First Development**: Implementation follows the defined specification in spec.md
- ✅ **Agentic Workflow**: Following spec → plan → tasks → implementation workflow
- ✅ **Clean, Readable Python**: Code will follow PEP 8 standards and be well-structured
- ✅ **Graceful Error Handling**: Proper validation and error responses will be implemented
- ✅ **Feature Completeness**: Will implement the complete authentication flow for dashboard

### Gate Conditions
- ✅ **Technology Standards**: Using FastAPI, SQLModel, and JWT as per existing architecture
- ✅ **Development Workflow**: Following spec → plan → tasks → implementation workflow

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-dashboard-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── health.py
│   ├── auth/
│   │   ├── middleware.py
│   │   └── jwt.py
│   ├── utils/
│   │   └── password.py
│   ├── database/
│   │   └── connection.py
│   └── config.py
└── tests/

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   └── globals.css
│   ├── components/
│   ├── services/
│   │   ├── api.ts
│   │   └── authService.ts
│   └── types/
└── tests/
```

**Structure Decision**: Full-stack web application with separate backend (FastAPI) and frontend (Next.js) directories, following modern web application architecture patterns.

## Phase 0: Research & Unknown Resolution

### Research Tasks

1. **Current Authentication Flow**: Understand how authentication works in the existing system
2. **Dashboard Route Analysis**: Identify why 401 errors occur on dashboard access
3. **Token Validation Mechanism**: Examine how JWT tokens are validated and persisted
4. **Frontend Route Protection**: Investigate patterns for protecting frontend routes in Next.js

### Findings from research.md
- Root cause: Missing frontend route protection on dashboard page
- Solution: Implement authentication guard in dashboard page
- Token validation: Use existing authService.isAuthenticated() method

## Phase 1: Design & Contracts

### Data Model Design

#### Authentication Token
- **Purpose**: Stores JWT token with expiration and user information
- **Fields**: token (string), expiration (datetime), user_id (string)
- **Relationships**: Associated with User entity in backend

#### Auth State
- **Purpose**: Tracks authentication status in frontend
- **Fields**: isAuthenticated (boolean), user (optional object), token (optional string)
- **State Transitions**: Unauthenticated → Authenticating → Authenticated/Unauthorized

### API Contract Design

#### GET /dashboard (Conceptual)
**Description**: Protected dashboard route that requires valid JWT token

**Headers**:
- Authorization: Bearer {token}

**Responses**:
- 200 OK: Successfully accessed dashboard (handled by frontend routing)
- 401 Unauthorized: Invalid or expired token

### Frontend Integration Points

1. **Dashboard Page**: Add authentication check and redirect logic
2. **AuthService**: Utilize existing isAuthenticated() method
3. **Navigation**: Implement proper redirect to login when unauthenticated

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
