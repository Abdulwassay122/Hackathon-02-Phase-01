# ADR-003: Toast Notification Implementation

**Status:** Accepted
**Date:** 2026-02-03

## Context

The application needs to provide immediate visual feedback to users for various operations including authentication success/failure, API responses, and system notifications. The solution must be accessible, consistent across the application, and easy to implement without excessive boilerplate code.

## Decision

We will use the `react-hot-toast` library for toast notifications. Specifically:

- Use react-hot-toast for its lightweight nature and Next.js compatibility
- Implement consistent positioning across the application (top-right)
- Define standard durations for different message types (success: 3s, error: 5s, info: 4s)
- Include accessibility features (ARIA labels, keyboard navigation support)
- Maintain consistent styling that matches the application theme

## Alternatives Considered

1. **react-toastify**: Popular alternative with more customization options but larger bundle size - rejected for performance reasons
2. **@radix-ui/react-toast**: Accessible component library but requires more setup - rejected for simplicity
3. **Custom implementation**: Build from scratch using React/Aria primitives - rejected for development time and maintenance overhead
4. **NextUI Toast**: Part of a larger component library - rejected to avoid adding a large UI library just for toasts

## Consequences

**Positive:**
- Lightweight library with minimal bundle impact
- Excellent Next.js compatibility
- Good accessibility features out of the box
- Easy to implement with minimal boilerplate
- Consistent UX across the application

**Negative:**
- Adds another dependency to the project
- Limited customization compared to custom solution
- Potential for library-specific API changes in future versions

## References

- `specs/5-app-stabilization/research.md` - Toast Notifications Library Choice decision
- `specs/5-app-stabilization/data-model.md` - Toast Notification entity
- `specs/5-app-stabilization/plan.md` - Technical Context section