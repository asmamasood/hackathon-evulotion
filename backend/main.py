"""
Main FastAPI application for the Todo application with Dapr integration
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from api.todos import router as todos_router
from api.auth import router as auth_router
from api.users import router as users_router
from api.chat import router as chat_router
from database.session import engine
from models.todo import Todo
from models.user import User
from sqlmodel import SQLModel
# from dapr.clients import DaprClient


# Global Dapr client instance
dapr_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the application
    """
    global dapr_client
    
    # Initialize Dapr client (Optional)
    try:
        from dapr.clients import DaprClient
        print("Initializing Dapr client...")
        dapr_client = DaprClient()
    except (ImportError, Exception) as e:
        print(f"Dapr client not initialized: {e}")
        dapr_client = None
    
    # Create tables on startup
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")
    yield
    
    # Cleanup on shutdown
    print("Shutting down...")
    if dapr_client:
        dapr_client.close()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Todo Application API - Phase III",
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
    return {"message": f"Welcome to {settings.app_name}", "version": "Phase III"}

# Health check endpoint
@app.get("/health")
async def health_check():
    health_status = {"status": "healthy", "service": "todo-backend"}
    if dapr_client:
        health_status["dapr"] = "connected"
    else:
        health_status["dapr"] = "not_available"
    return health_status


# Function to get Dapr client (for dependency injection)
def get_dapr_client():
    global dapr_client
    if dapr_client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dapr client not initialized"
        )
    return dapr_client


def dev():
    """Development entry point"""
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )