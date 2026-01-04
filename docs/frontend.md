# Frontend Documentation

## Project Structure
```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   │   ├── (auth)/    # Authentication pages
│   │   │   ├── login/
│   │   │   └── register/
│   │   └── dashboard/ # Main dashboard page
│   ├── components/    # Reusable React components
│   ├── services/      # API service utilities
│   ├── styles/        # Global styles
│   └── lib/           # Utility libraries
├── public/            # Static assets
└── package.json       # Dependencies and scripts
```

## Key Components

### Layout Components
- `Layout.tsx` - Main application layout with navigation
- `MobileNav.tsx` - Responsive mobile navigation

### Task Components
- `TaskList.tsx` - Displays list of tasks
- `TaskForm.tsx` - Form for creating/editing tasks
- `TaskItem.tsx` - Individual task display and actions

### Utility Components
- `LoadingSpinner.tsx` - Loading state indicator
- `ErrorDisplay.tsx` - Error message display
- `ProtectedRoute.tsx` - Authentication wrapper

## Services

### API Service
- `apiService` - Handles all API communication with JWT token management
- `taskService` - Task-specific API operations
- `authService` - Authentication operations

### Session Management
- `sessionManager` - Manages authentication state

## Styling
- Uses Tailwind CSS for styling
- Responsive design with mobile-first approach
- Global styles in `src/styles/globals.css`

## Pages

### Authentication
- `/login` - User login page
- `/register` - User registration page

### Main Application
- `/dashboard` - Main task management page
- `/profile` - User profile page (placeholder)