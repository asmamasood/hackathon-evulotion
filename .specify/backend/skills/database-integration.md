# Database Integration Skill

## Purpose
Manage database interactions with FastAPI, including schema design, operations, and migrations.

## Implementation Guidelines
- Use SQLAlchemy with async support for database operations
- Implement proper connection pooling
- Design efficient database schemas
- Handle transactions appropriately
- Implement proper error handling for database operations

## Best Practices
- Use Alembic for database migrations
- Implement repository pattern for data access
- Optimize queries with proper indexing
- Use connection pooling for performance
- Implement proper data validation

## Example Usage
```
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```