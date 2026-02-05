# ADR-001: Authentication Architecture

**Status:** Accepted
**Date:** 2026-02-03

## Context

The application needs to securely authenticate users and maintain their session state across page navigations. We need to decide how to handle authentication tokens, session persistence, and secure communication between frontend and backend. The solution must prevent unauthorized access to protected routes while providing a smooth user experience.

## Decision

We will use a combination of cookies for persistent authentication and React context for client-side state management. Specifically:

- JWT tokens will be stored in httpOnly cookies for security
- Authentication state (isAuthenticated, user data) will be maintained in React Context
- Next.js middleware will handle server-side route protection
- Client-side ProtectedRoute components will provide additional UX benefits

## Alternatives Considered

1. **Local storage only**: Store JWT in localStorage - rejected due to XSS vulnerability risk
2. **Session storage only**: Store JWT in sessionStorage - rejected due to non-persistence across browser sessions
3. **Token in memory only**: Store in React state only - rejected due to loss on page refresh
4. **JWT in cookies with httpOnly flag**: Most secure but requires more complex token refresh handling

## Consequences

**Positive:**
- Enhanced security through httpOnly cookies preventing XSS token theft
- Smooth UX with client-side state management reducing server round trips
- Proper session persistence across page refreshes
- Server-side protection through Next.js middleware

**Negative:**
- More complex implementation with dual-layer state management
- Potential for state inconsistency between cookie and context
- Increased complexity in token refresh handling

## References

- `specs/5-app-stabilization/research.md` - Authentication State Management decision
- `specs/5-app-stabilization/data-model.md` - Authentication State entity
- `specs/5-app-stabilization/plan.md` - Technical Context section