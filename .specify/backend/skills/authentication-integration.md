# Authentication Integration Skill

## Purpose
Integrate secure authentication and authorization mechanisms with FastAPI endpoints.

## Implementation Guidelines
- Implement JWT token authentication using middleware or dependencies
- Create secure login/logout endpoints
- Integrate with existing auth system (e.g., the auth agent)
- Implement role-based access control
- Handle token refresh and validation

## Security Considerations
- Use HTTPS in production environments
- Implement proper token storage and transmission
- Secure sensitive endpoints with authentication dependencies
- Implement proper session management
- Follow OWASP authentication security standards

## Example Usage
```
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/secure-endpoint")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
```