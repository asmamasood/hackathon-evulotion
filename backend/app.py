# Hugging Face Space app for Todo Application Backend

import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from .core.config import settings
from .api.todos import router as todos_router
from .api.auth import router as auth_router
from .api.users import router as users_router
from .api.chat import router as chat_router
from .database.session import engine
from .models.todo import Todo
from .models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the application
    """
    # Create tables on startup
    print("Creating database tables...")
    # For Hugging Face Spaces, we'll use a simpler approach
    # In a real implementation, you'd handle database initialization differently
    yield
    # Cleanup on shutdown if needed
    print("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Todo Application API - Deployed on Hugging Face Spaces",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(todos_router, prefix="/api/v1", tags=["todos"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}", "deployment": "huggingface-spaces"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-backend", "deployment": "huggingface"}


# For Hugging Face Spaces, we need to define the main entry point
def main():
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7860)),
        reload=False  # Disable reload in production
    )


if __name__ == "__main__":
    main()