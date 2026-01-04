# Todo Application - Full Stack Web App

A modern full-stack todo application with a Next.js frontend and FastAPI backend, featuring responsive UI with Tailwind CSS and standardized uv-managed virtual environment for backend development.

## Features

- **Modern UI**: Responsive design with Tailwind CSS for mobile, tablet, and desktop
- **Task Management**: Full CRUD operations (Create, Read, Update, Delete) for tasks
- **Task Status**: Toggle task completion status with visual feedback
- **Real-time Updates**: Immediate visual feedback for all user actions
- **Loading States**: Clear loading indicators for API operations
- **Error Handling**: User-friendly error messages and success feedback
- **Responsive Design**: Works seamlessly across all device sizes

## Prerequisites

- Python 3.13+
- uv (Python package manager)
- Node.js 18+ (for frontend development)

## Backend Setup with uv

### 1. Install uv (if not already installed)
```bash
pip install uv
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
source .venv/Scripts/activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install backend dependencies
```bash
# With virtual environment activated
uv pip install fastapi uvicorn python-multipart sqlmodel python-jose[cryptography] better-exceptions
```

### 4. Install from pyproject.toml (if available)
```bash
# If pyproject.toml exists in project root
uv sync
```

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
# or
yarn install
```

### 3. Run development server
```bash
npm run dev
# or
yarn dev
```

## Running the Application

### 1. Start the backend server
```bash
# Make sure virtual environment is activated
uvicorn backend.src.api.main:app --reload --port 8000
```

### 2. Start the frontend (in a separate terminal)
```bash
cd frontend
npm run dev
```

### 3. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API docs: http://localhost:8000/docs

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── auth/           # Authentication middleware
│   ├── requirements.txt    # Python dependencies
│   └── main.py             # Application entry point
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   └── services/       # API service layer
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind CSS configuration
├── pyproject.toml          # Backend dependencies for uv
└── README.md               # This file
```

## Development Workflow

### Backend Development
1. Activate the uv virtual environment
2. Make changes to Python files in `backend/src/`
3. The server will auto-reload with `--reload` flag

### Frontend Development
1. Make changes to React/Next.js files in `frontend/src/`
2. The development server will hot-reload changes
3. Use Tailwind CSS utility classes for styling

## API Endpoints

- `GET /api/tasks` - Retrieve all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update an existing task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Testing

### Backend Tests
```bash
# Run backend tests (with virtual environment activated)
python -m pytest backend/tests/
```

### Frontend Tests
```bash
# Run frontend tests
cd frontend
npm test
```

## Deployment

### Backend
The backend can be deployed to any Python-compatible hosting platform. Make sure to install dependencies using uv in the deployment environment.

### Frontend
The frontend can be built for production using:
```bash
cd frontend
npm run build
```

## Notes

- The application uses a standardized uv-managed virtual environment for consistent backend dependency management
- All UI components are built with Tailwind CSS for a modern, responsive design
- API contracts remain unchanged to maintain backward compatibility
- Authentication is implemented using JWT tokens