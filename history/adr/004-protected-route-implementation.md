# ADR-004: Protected Route Implementation

**Status:** Accepted
**Date:** 2026-02-03

## Context

The application needs to protect certain routes (like the dashboard) from unauthorized access while providing a smooth user experience. Unauthorized users should be redirected to the login page, while authenticated users should have seamless access. The solution must work on both client and server side and handle loading states appropriately.

## Decision

We will implement a hybrid approach using both Next.js middleware for server-side protection and client-side ProtectedRoute components. Specifically:

- Next.js middleware will handle server-side route protection
- Client-side ProtectedRoute React component will provide enhanced UX with loading states
- Centralized authentication state will be used by both mechanisms
- Proper loading states will be shown during authentication checks
- Graceful handling of authentication failures with clear user feedback

## Alternatives Considered

1. **Server-side only**: Use only Next.js middleware - rejected as it doesn't provide smooth client-side UX
2. **Client-side only**: Use only ProtectedRoute components - rejected as it allows brief access before redirect
3. **Higher-Order Component (HOC)**: Traditional React pattern - rejected for newer hook/component-based approach
4. **Custom hooks**: useAuth hook in each component - rejected as it duplicates protection logic

## Consequences

**Positive:**
- Layered security with both server and client protection
- Smooth user experience with loading states
- Centralized authentication logic
- Proper SEO handling with server-side redirects

**Negative:**
- More complex implementation with dual-layer protection
- Potential for inconsistent behavior if client and server logic diverge
- Additional complexity in authentication state synchronization

## References

- `specs/5-app-stabilization/research.md` - Protected Route Implementation decision
- `specs/5-app-stabilization/quickstart.md` - ProtectedRoute component reference
- `specs/5-app-stabilization/plan.md` - Technical Context section