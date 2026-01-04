# Claude Code Rules - Frontend

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in frontend development for the Todo App.

## Task context

**Your Surface:** You operate on the frontend level, providing guidance to users and executing development tasks for the Next.js frontend.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Frontend components are responsive and accessible
- API integrations work seamlessly with the backend
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Frontend follows Next.js 16+ best practices
- Components are reusable and well-structured
- TypeScript is used for type safety
- Responsive design works on all screen sizes
- Proper error handling and loading states are implemented

## Development Guidelines

### 1. Frontend Architecture:
- Use Next.js App Router for routing
- Implement responsive design with Tailwind CSS
- Create reusable components in the components/ directory
- Use TypeScript for all components and services
- Follow React best practices for state management

### 2. API Integration:
- Use the apiService for all backend communication
- Implement proper error handling for API calls
- Add loading states for all asynchronous operations
- Handle authentication tokens automatically

### 3. Component Structure:
- Create small, focused components
- Use proper TypeScript interfaces
- Implement proper accessibility attributes
- Follow consistent styling patterns

### 4. Error Handling:
- Implement error boundaries where appropriate
- Show user-friendly error messages
- Provide retry mechanisms for failed operations
- Handle network errors gracefully

### 5. Performance:
- Optimize component rendering
- Use proper React hooks
- Implement code splitting where appropriate
- Optimize images and assets

## Code Standards
- Follow React and Next.js best practices
- Use TypeScript for type safety
- Implement proper component documentation
- Write clean, readable code
- Follow accessibility guidelines