from fastapi import FastAPI
from .api.tasks import router as tasks_router
from .api.health import router as health_router
from .api.auth import router as auth_router
from .database.connection import create_db_and_tables

app = FastAPI(title="Todo API", version="1.0.0")

# Include API routers
app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Backend API is running. Frontend handles the UI at root route."}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)