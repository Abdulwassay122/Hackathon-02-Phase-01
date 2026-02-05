# Feature Specification: Fix Task API 401 Authentication & Migrate DB to Neon PostgreSQL

**Feature Branch**: `007-fix-task-api-auth`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Fix unauthorized (401) responses from the Task API when called from the frontend and Postman using JWT tokens, and migrate the backend database from SQLite to Neon PostgreSQL using an environment-based connection string."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Task API with Valid JWT (Priority: P1)

As an authenticated user, I want to access the Task API using my JWT token so that I can create, read, update, and delete my tasks from both the frontend application and external tools like Postman.

**Why this priority**: This is the core functionality that enables users to interact with their tasks securely. Without this, the entire task management system becomes unusable.

**Independent Test**: Can be fully tested by making authenticated API calls with valid JWT tokens from both frontend and Postman, and verifying successful responses (200/201) for all task operations.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token, **When** user makes API request to task endpoints with Authorization header, **Then** API returns success status (200/201) and performs requested operation
2. **Given** user has valid JWT token, **When** user accesses tasks via frontend application, **Then** tasks load successfully without authentication errors

---

### User Story 2 - Handle Invalid JWT Tokens Properly (Priority: P2)

As an application administrator, I want the API to properly reject invalid or missing JWT tokens with appropriate error responses so that unauthorized access is prevented and proper error handling occurs.

**Why this priority**: Security is paramount for protecting user data. Proper error responses help developers diagnose authentication issues quickly.

**Independent Test**: Can be tested by making API requests with invalid/malformed/expired JWT tokens and verifying appropriate 401 Unauthorized responses.

**Acceptance Scenarios**:

1. **Given** user sends request without JWT token, **When** request reaches protected task endpoints, **Then** API returns 401 Unauthorized error
2. **Given** user sends request with invalid/expired JWT token, **When** request reaches protected task endpoints, **Then** API returns 401 Unauthorized error

---

### User Story 3 - Enforce User Task Ownership (Priority: P3)

As a user, I want the API to enforce that I can only access my own tasks so that my data remains private and secure from other users.

**Why this priority**: Data privacy and security is critical for user trust. Users should not be able to access tasks belonging to other users.

**Independent Test**: Can be tested by attempting to access tasks with a valid JWT but for a different user ID than what's in the token.

**Acceptance Scenarios**:

1. **Given** user has valid JWT token for user A, **When** user attempts to access tasks for user B, **Then** API returns 403 Forbidden error
2. **Given** user has valid JWT token for user A, **When** user accesses their own tasks, **Then** API returns 200 OK with requested tasks

---

### User Story 4 - Use PostgreSQL Database for Persistence (Priority: P1)

As a system administrator, I want the backend to use Neon PostgreSQL instead of SQLite so that the application can scale with production-level database capabilities.

**Why this priority**: Moving from SQLite to PostgreSQL is essential for production readiness, allowing for better performance, concurrency, and reliability.

**Independent Test**: Can be tested by verifying that the application connects to PostgreSQL using the DATABASE_URL environment variable and that tasks persist across server restarts.

**Acceptance Scenarios**:

1. **Given** DATABASE_URL is configured for Neon PostgreSQL, **When** application starts, **Then** it connects to PostgreSQL database successfully
2. **Given** tasks exist in PostgreSQL database, **When** application server restarts, **Then** tasks remain accessible and persistent

### Edge Cases

- What happens when JWT token has malformed payload but valid signature?
- How does system handle database connection failures during API requests?
- What occurs when the database URL in environment variables is invalid or unreachable?
- How does system behave when user ID in JWT doesn't correspond to an existing user in the database?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read JWT from `Authorization: Bearer <token>` header for all task API endpoints
- **FR-002**: System MUST verify JWT token signature using shared secret from `BETTER_AUTH_SECRET` environment variable
- **FR-003**: System MUST decode JWT payload to extract user ID and email information for authentication
- **FR-004**: System MUST reject requests without valid JWT tokens with 401 Unauthorized status
- **FR-005**: System MUST enforce user ownership by comparing JWT user ID with route/user parameters
- **FR-006**: System MUST connect to PostgreSQL database using DATABASE_URL environment variable instead of SQLite
- **FR-007**: System MUST store and retrieve task data exclusively from PostgreSQL database
- **FR-008**: System MUST return 403 Forbidden when JWT user ID doesn't match requested resource user ID
- **FR-009**: System MUST filter all task queries by the authenticated user's ID from JWT token
- **FR-010**: System MUST create necessary database tables in PostgreSQL if they don't exist on startup

### Key Entities

- **JWT Token**: Represents user authentication credentials containing user ID, email, and expiration time
- **Task**: Represents user's individual task items with ownership tied to authenticated user
- **User**: Identity associated with JWT token and task ownership relationship

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully access task API endpoints with valid JWT tokens returning 200/201 status codes
- **SC-002**: Requests without valid JWT tokens consistently return 401 Unauthorized status codes
- **SC-003**: Requests with valid JWT tokens but wrong user context return 403 Forbidden status codes
- **SC-004**: Task data persists in PostgreSQL database and survives application restarts
- **SC-005**: All task operations are properly filtered by authenticated user ID ensuring proper data isolation
- **SC-006**: Application successfully connects to PostgreSQL using environment variable configuration
- **SC-007**: No SQLite database files are created or accessed after implementation
