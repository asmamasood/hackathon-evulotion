# Hugging Face Space for Todo Application Backend

import os
import subprocess
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from core.config import settings
from api.todos import router as todos_router
from api.auth import router as auth_router
from api.users import router as users_router
from api.chat import router as chat_router
from database.session import engine
from models.todo import Todo
from models.user import User


# For Hugging Face Spaces, we'll set up the application differently
# We'll use a simpler approach that works well in the Spaces environment

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the application
    """
    print("Initializing Todo Application Backend for Hugging Face Spaces...")
    
    # For Spaces, we'll use a simple initialization
    # In a real implementation, you'd handle database initialization appropriately
    yield
    
    print("Shutting down...")


app = FastAPI(
    title="Todo Application Backend - Hugging Face Space",
    version="1.0.0",
    description="Todo Application API running on Hugging Face Spaces",
    lifespan=lifespan
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(todos_router, prefix="/api/v1", tags=["todos"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Todo Application Backend",
        "deployment": "huggingface-spaces",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "todo-backend",
        "deployment": "huggingface-spaces"
    }

# For Hugging Face Spaces, we'll also create a Gradio interface wrapper
def run_gradio_interface():
    """
    Alternative interface using Gradio for Hugging Face Spaces
    """
    try:
        import gradio as gr
        import requests
        import json
        
        def query_api(endpoint, method="GET", data=None):
            """
            Generic function to query the FastAPI endpoints
            """
            base_url = f"http://localhost:{os.getenv('PORT', 7860)}"
            url = f"{base_url}{endpoint}"
            
            headers = {"Content-Type": "application/json"}
            
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=headers, json=data)
                elif method.upper() == "PUT":
                    response = requests.put(url, headers=headers, json=data)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers)
                elif method.upper() == "PATCH":
                    response = requests.patch(url, headers=headers, json=data)
                else:
                    return f"Unsupported method: {method}"
                
                return json.dumps(response.json(), indent=2)
            except Exception as e:
                return f"Error querying API: {str(e)}"
        
        with gr.Blocks() as demo:
            gr.Markdown("# Todo Application Backend API")
            gr.Markdown("This is a Hugging Face Space hosting the Todo Application backend API")
            
            with gr.Tab("API Query"):
                endpoint = gr.Textbox(label="Endpoint", placeholder="/health or /api/v1/users/me")
                method = gr.Dropdown(choices=["GET", "POST", "PUT", "DELETE", "PATCH"], value="GET", label="HTTP Method")
                data_input = gr.Textbox(label="JSON Data (for POST/PUT/PATCH)", placeholder='{"key": "value"}')
                query_btn = gr.Button("Query API")
                output = gr.JSON(label="Response")
                
                query_btn.click(
                    fn=lambda ep, mtd, dt: query_api(ep, mtd, json.loads(dt) if dt else None),
                    inputs=[endpoint, method, data_input],
                    outputs=output
                )
            
            with gr.Tab("Documentation"):
                gr.Markdown("""
                ## Available Endpoints
                
                ### Todo Endpoints
                - `GET /api/v1/{user_id}/todos` - Get user's todos
                - `POST /api/v1/{user_id}/todos` - Create new todo
                - `GET /api/v1/{user_id}/todos/{todo_id}` - Get specific todo
                - `PUT /api/v1/{user_id}/todos/{todo_id}` - Update todo
                - `DELETE /api/v1/{user_id}/todos/{todo_id}` - Delete todo
                - `PATCH /api/v1/{user_id}/todos/{todo_id}/complete` - Toggle completion
                
                ### Auth Endpoints
                - `POST /api/v1/login` - Login
                - `POST /api/v1/register` - Register
                - `GET /api/v1/me` - Get current user
                
                ### Health Check
                - `GET /` - Root endpoint
                - `GET /health` - Health check
                """)
        
        return demo
    except ImportError:
        print("Gradio not available, running FastAPI only")
        return None


# Initialize Gradio interface if available
gradio_interface = run_gradio_interface()


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # For Hugging Face Spaces, run with the port specified by the environment
    port = int(os.getenv("PORT", 7860))
    
    # If Gradio is available, we can run both
    if gradio_interface:
        # Run Gradio in a separate thread/process
        import threading
        import time
        
        def run_gradio():
            gradio_interface.launch(server_name="0.0.0.0", server_port=port+1, share=False)
        
        gradio_thread = threading.Thread(target=run_gradio, daemon=True)
        gradio_thread.start()
        
        # Give Gradio a moment to start
        time.sleep(2)
    
    # Run the FastAPI application
    uvicorn.run(
        "space:app",  # Use 'space:app' since this file is space.py
        host="0.0.0.0",
        port=port,
        log_level="info"
    )