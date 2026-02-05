# Implementation Tasks: Fix Task API 401 Authentication & Migrate DB to Neon PostgreSQL

## Feature Overview
This feature addresses critical authentication issues in the Task API by implementing proper JWT token validation and migrating the database from SQLite to PostgreSQL. The implementation will involve updating the authentication middleware to correctly read JWT tokens from the Authorization header, validate them using the shared secret, and enforce proper user ownership by filtering task queries based on the authenticated user. Additionally, the database configuration will be updated to use PostgreSQL with environment-based connection strings instead of SQLite.

## Phase 1: Setup
Goal: Prepare the development environment and update dependencies for PostgreSQL and JWT validation.

- [x] T001 Update requirements.txt with PostgreSQL dependencies (psycopg2-binary) and JWT validation libraries
- [x] T002 [P] Update .env file to remove SQLite connection string and add DATABASE_URL for PostgreSQL
- [x] T003 [P] Install PostgreSQL client libraries in the backend environment

## Phase 2: Foundational Infrastructure
Goal: Implement core authentication and database connection infrastructure that will be used by all user stories.

- [x] T004 [P] [US4] Update database connection in backend/src/database/connection.py to use DATABASE_URL for PostgreSQL instead of SQLite
- [x] T005 [P] [US4] Modify SQLModel engine creation to use PostgreSQL dialect and ensure table creation works properly
- [x] T006 [P] [US1] Create JWT validation utility in backend/src/utils/jwt.py to decode and validate JWT tokens using BETTER_AUTH_SECRET
- [x] T007 [P] [US1] Implement authentication middleware in backend/src/auth/middleware.py to extract and validate JWT from Authorization header
- [x] T008 [P] [US1] Update backend/src/models/task.py to include proper foreign key relationship with User model
- [x] T009 [P] [US1] Update backend/src/models/user.py with proper User model definition for PostgreSQL

## Phase 3: User Story 1 - Access Task API with Valid JWT (Priority: P1)
Goal: Enable authenticated users to access the Task API using JWT tokens from frontend and Postman with successful responses (200/201).

Independent Test: Making authenticated API calls with valid JWT tokens from both frontend and Postman, and verifying successful responses (200/201) for all task operations.

- [x] T010 [US1] Integrate authentication middleware with main FastAPI application in backend/src/main.py
- [x] T011 [P] [US1] Update GET /api/tasks/{user_id} endpoint in backend/src/api/tasks.py to validate JWT and filter tasks by authenticated user
- [x] T012 [P] [US1] Update POST /api/tasks/{user_id} endpoint in backend/src/api/tasks.py to validate JWT and assign user_id from token
- [x] T013 [P] [US1] Update GET /api/tasks/{user_id}/{task_id} endpoint in backend/src/api/tasks.py to validate JWT and check task ownership
- [x] T014 [P] [US1] Update PUT /api/tasks/{user_id}/{task_id} endpoint in backend/src/api/tasks.py to validate JWT and check task ownership
- [x] T015 [P] [US1] Update DELETE /api/tasks/{user_id}/{task_id} endpoint in backend/src/api/tasks.py to validate JWT and check task ownership
- [x] T016 [P] [US1] Implement proper error responses for authentication failures in backend/src/api/tasks.py
- [ ] T017 [US1] Test API access with valid JWT from frontend and verify successful responses (200/201)

## Phase 4: User Story 2 - Handle Invalid JWT Tokens Properly (Priority: P2)
Goal: Ensure the API properly rejects invalid or missing JWT tokens with appropriate 401 Unauthorized responses for security.

Independent Test: Making API requests with invalid/malformed/expired JWT tokens and verifying appropriate 401 Unauthorized responses.

- [x] T018 [US2] Implement validation for missing JWT tokens in authentication middleware
- [x] T019 [US2] Implement validation for malformed JWT tokens in authentication middleware
- [x] T020 [US2] Implement validation for expired JWT tokens in authentication middleware
- [x] T021 [US2] Ensure proper 401 Unauthorized responses for all invalid JWT scenarios
- [ ] T022 [US2] Test API access with missing JWT tokens and verify 401 responses
- [ ] T023 [US2] Test API access with invalid/expired JWT tokens and verify 401 responses

## Phase 5: User Story 3 - Enforce User Task Ownership (Priority: P3)
Goal: Implement proper user ownership enforcement to ensure users can only access their own tasks for data privacy.

Independent Test: Attempting to access tasks with a valid JWT but for a different user ID than what's in the token.

- [x] T024 [US3] Implement user ID comparison logic in authentication middleware to validate JWT user ID against route user ID
- [x] T025 [US3] Update all task endpoints to return 403 Forbidden when JWT user ID doesn't match requested user ID
- [x] T026 [US3] Add proper user ID validation in task retrieval functions
- [ ] T027 [US3] Test cross-user access with valid JWT but wrong user context and verify 403 Forbidden responses
- [ ] T028 [US3] Test access to user's own tasks with valid JWT and verify successful responses (200 OK)

## Phase 6: User Story 4 - Use PostgreSQL Database for Persistence (Priority: P1)
Goal: Migrate the backend to use Neon PostgreSQL instead of SQLite for production-level database capabilities.

Independent Test: Verifying that the application connects to PostgreSQL using the DATABASE_URL environment variable and that tasks persist across server restarts.

- [x] T029 [US4] Test database connection to PostgreSQL using DATABASE_URL configuration
- [x] T030 [US4] Verify that task tables are created in PostgreSQL on application startup
- [ ] T031 [US4] Create tasks and verify they're stored in PostgreSQL database
- [ ] T032 [US4] Restart application and verify tasks persist in PostgreSQL database
- [x] T033 [US4] Confirm that no SQLite files are created or accessed after implementation
- [ ] T034 [US4] Verify all CRUD operations work correctly with PostgreSQL database

## Phase 7: Polish & Cross-Cutting Concerns
Goal: Complete the implementation by addressing remaining integration points and ensuring all components work together seamlessly.

- [ ] T035 Update frontend/src/services/api.ts to ensure proper JWT header formatting for API requests
- [x] T036 Update backend/src/api/tasks.py to include proper logging for authentication events
- [x] T037 [P] Add environment validation in backend/src/main.py to ensure DATABASE_URL is properly configured
- [ ] T038 Update documentation with new database configuration requirements
- [ ] T039 Perform comprehensive testing of all API endpoints with various JWT scenarios
- [ ] T040 Verify all acceptance criteria from user stories are satisfied
- [ ] T041 Run end-to-end tests to ensure frontend and backend work together with JWT authentication
- [x] T042 Update any remaining references to SQLite in the codebase

## Dependencies
- User Story 1 (P1) and User Story 4 (P1) can be developed in parallel as foundational requirements
- User Story 2 (P2) depends on User Story 1 for authentication infrastructure
- User Story 3 (P3) depends on User Story 1 for authentication infrastructure

## Parallel Execution Examples
Per User Story:
- User Story 1: Tasks T011-T015 can be executed in parallel as they each handle a different API endpoint
- User Story 4: Tasks T029-T033 can be executed in parallel as they each test a different aspect of PostgreSQL integration
- User Story 2: Tasks T018-T023 can be executed in parallel as they each test a different authentication failure scenario

## Implementation Strategy
1. Start with Phase 1-2 to establish the foundational infrastructure (MVP baseline)
2. Implement User Story 1 (P1) to get core functionality working
3. Implement User Story 4 (P1) to complete the database migration
4. Implement User Story 2 (P2) and User Story 3 (P3) for enhanced security
5. Complete with Phase 7 for polish and integration testing

The MVP scope includes just the foundational setup (Phase 1-2) and User Story 1 (P1) to get JWT authentication working with basic task operations, which will satisfy the core requirement of accessing the Task API with valid JWT tokens.