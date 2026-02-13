# Error Handling Skill

## Purpose
Implement comprehensive error handling for FastAPI applications.

## Implementation Guidelines
- Create custom exception handlers
- Return appropriate HTTP status codes
- Log errors appropriately without exposing sensitive information
- Implement centralized error handling
- Provide meaningful error messages to clients

## Best Practices
- Use HTTPException for standard HTTP errors
- Create custom exception classes for application-specific errors
- Implement global exception handlers
- Log errors with appropriate severity levels
- Sanitize error messages for client responses

## Example Usage
```
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )

class BusinessLogicError(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(BusinessLogicError)
async def business_logic_exception_handler(request: Request, exc: BusinessLogicError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )
```