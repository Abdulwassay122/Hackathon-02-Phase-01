# Quickstart Guide: UI Modernization & Backend UV Environment

## Prerequisites
- Python 3.13+
- uv package manager
- Node.js (for Tailwind CSS compilation, if needed)
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
uv pip install fastapi uvicorn python-multipart

# Verify installation
python -c "import fastapi; print('FastAPI installed successfully')"
```

### 3. Install Tailwind CSS (for frontend)
```bash
# If using Node.js for Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 4. Run the Application
```bash
# Activate virtual environment
source .venv/bin/activate  # or appropriate activation command for your OS

# Start the backend server
uvicorn backend.main:app --reload --port 8000

# In a separate terminal, serve the frontend
# (instructions will vary based on your frontend setup)
```

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
- All environment variables should be documented in a .env.example file

## Troubleshooting
- If uv is not installed: `pip install uv`
- If virtual environment activation fails: Check your shell and use appropriate activation command
- If dependencies fail to install: Ensure Python 3.13+ is installed