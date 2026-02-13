# FastAPI Routing Skill

## Purpose
Design and implement efficient FastAPI routing with proper request/response handling.

## Implementation Guidelines
- Use Pydantic models for request/response validation
- Implement proper HTTP status codes
- Follow RESTful API design principles
- Use path and query parameters appropriately
- Implement proper error handling with custom exceptions

## Best Practices
- Separate concerns with APIRouter for different modules
- Use dependency injection for shared functionality
- Implement rate limiting where appropriate
- Document endpoints with OpenAPI specifications

## Example Usage
```
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()

class UserRequest(BaseModel):
    name: str
    email: str

@router.post("/users/", status_code=201)
async def create_user(request: UserRequest):
    # Implementation here
    return {"message": "User created"}
```