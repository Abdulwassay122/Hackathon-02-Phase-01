# Implementation Tasks: Fix 401 Unauthorized Error on Dashboard

**Feature**: 001-fix-dashboard-auth
**Created**: 2026-02-03
**Status**: Ready for Implementation

## Dependencies

- **User Story 2 depends on User Story 1**: Unauthenticated user redirect requires the authentication guard to be working
- **User Story 3 depends on User Story 1**: Token validation requires the dashboard page to be properly protected

## Parallel Execution Opportunities

- Frontend route protection can proceed in parallel with backend token validation verification
- Testing tasks can run in parallel with implementation tasks once the core functionality is in place
- Dashboard page updates can be worked on independently once the auth service is confirmed working

## Implementation Strategy

**MVP Scope**: Implement User Story 1 (Authenticated User Access) with minimal viable functionality - just the authentication guard on the dashboard page.

**Incremental Delivery**:
- Phase 1: Setup and foundational tasks
- Phase 2: Core dashboard authentication protection
- Phase 3: Enhanced token validation and error handling
- Phase 4: Testing and polish

---

## Phase 1: Setup

- [ ] T001 Create contracts directory if not exists in specs/001-fix-dashboard-auth/contracts/

## Phase 2: Foundational Tasks

- [ ] T002 [P] Prepare frontend authentication service for dashboard protection in frontend/src/services/authService.ts
- [ ] T003 [P] Verify backend authentication middleware is functioning in backend/src/auth/middleware.py
- [ ] T004 [P] Identify dashboard page location for route protection in frontend/src/app/dashboard/page.tsx

## Phase 3: User Story 1 - Authenticated User Access (Priority: P1)

**Goal**: An authenticated user visits the dashboard and expects to see their content without encountering authentication errors. The user should be able to access the dashboard and interact with it normally, with their authentication state persisting across page refreshes.

**Independent Test**: Log in successfully, navigate to /dashboard, verify the page loads without 401 errors, refresh the page and confirm access remains available.

- [ ] T005 [P] [US1] Create dashboard authentication guard implementation plan in frontend/src/app/dashboard/page.tsx
- [ ] T006 [US1] Implement useEffect hook to check authentication status in frontend/src/app/dashboard/page.tsx
- [ ] T007 [US1] Add redirect to login for unauthenticated users in frontend/src/app/dashboard/page.tsx
- [ ] T008 [US1] Add loading state to prevent content flash in frontend/src/app/dashboard/page.tsx
- [ ] T009 [US1] Test authenticated user access to dashboard
- [ ] T010 [US1] Verify auth state persists across page refreshes in frontend/src/app/dashboard/page.tsx

## Phase 4: User Story 2 - Unauthenticated User Redirect (Priority: P2)

**Goal**: An unauthenticated user attempts to access the dashboard and should be redirected to the login page instead of seeing an error. This provides a smooth user experience by guiding users to authenticate when needed.

**Independent Test**: Navigate to /dashboard without authentication, verify automatic redirect to /login page.

- [ ] T011 [P] [US2] Implement authentication check in dashboard page in frontend/src/app/dashboard/page.tsx
- [ ] T012 [US2] Add conditional rendering for unauthenticated state in frontend/src/app/dashboard/page.tsx
- [ ] T013 [US2] Test redirect functionality for unauthenticated users
- [ ] T014 [US2] Verify redirect happens immediately on page load in frontend/src/app/dashboard/page.tsx

## Phase 5: User Story 3 - Consistent Token Validation (Priority: P3)

**Goal**: The system should consistently validate JWT tokens and return appropriate HTTP status codes (401) for invalid or expired tokens. This ensures predictable behavior across all authentication scenarios.

**Independent Test**: Use an expired or malformed token to access /dashboard and verify consistent 401 responses.

- [ ] T015 [P] [US3] Add token validation logic to authService in frontend/src/services/authService.ts
- [ ] T016 [US3] Implement token expiration check in frontend/src/services/authService.ts
- [ ] T017 [US3] Add error handling for invalid tokens in frontend/src/app/dashboard/page.tsx
- [ ] T018 [US3] Test with expired tokens
- [ ] T019 [US3] Test with malformed tokens

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T020 Test complete authentication flow with valid credentials
- [ ] T021 Test error scenarios (invalid tokens, expired tokens)
- [ ] T022 Verify no regression in existing authentication functionality
- [ ] T023 Update documentation if needed
- [ ] T024 Run full test suite to ensure no regressions