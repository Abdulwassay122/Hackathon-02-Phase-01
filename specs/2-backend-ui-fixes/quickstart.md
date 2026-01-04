# Quickstart Guide: Backend Fixes & UI Enhancement

## Prerequisites
- Python 3.13+
- uv package manager
- Node.js (for Tailwind CSS compilation)
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Backend Environment
```bash
# Navigate to project root
cd <project-root>

# Create virtual environment using uv
uv venv

# Activate the virtual environment
# On Windows:
source .venv/Scripts/activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install fastapi uvicorn python-multipart sqlmodel python-jose[cryptography]

# Verify installation
python -c "import fastapi; print('FastAPI installed successfully')"
```

### 3. Set up Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build Tailwind CSS
npx tailwindcss -i ./src/styles/globals.css -o ./dist/output.css
```

### 4. Run the Application
```bash
# Terminal 1: Start the backend server
cd backend
# Make sure virtual environment is activated
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start the frontend development server
cd frontend
npm run dev
```

## Running with Authentication
The application now requires authentication. To access protected routes:

1. Navigate to the root route (`/`) to see the login form
2. Authenticate with valid credentials
3. The system will issue a JWT token
4. All subsequent API requests will include the authentication token

## Development Workflow

### Backend Development
1. Activate the uv virtual environment
2. Make changes to Python files
3. The server will auto-reload with `--reload` flag

### Frontend Development
1. Update HTML/CSS/JS files
2. If using Tailwind CSS, run the build process:
   ```bash
   npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
   ```

## Environment Configuration
- Backend runs on http://localhost:8000 by default
- Frontend should be configured to communicate with the backend API
- Authentication tokens are stored in browser's local storage

## Troubleshooting
- If uv is not installed: `pip install uv`
- If virtual environment activation fails: Check your shell and use appropriate activation command
- If dependencies fail to install: Ensure Python 3.13+ is installed
- For module import errors: Run the application as a module using `python -m backend.src.main`