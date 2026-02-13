# Neon Serverless Integration Skill

## Purpose
Integrate effectively with Neon Serverless PostgreSQL features and capabilities.

## Implementation Guidelines
- Leverage Neon's branching and cloning features for development workflows
- Configure connection pooling appropriately for serverless environment
- Handle connection lifecycle properly in application code
- Use Neon's built-in analytics and monitoring
- Implement proper error handling for connection interruptions

## Best Practices
- Use connection pooling libraries (like pgBouncer or built-in poolers)
- Implement retry logic for transient connection failures
- Monitor compute startup times in serverless mode
- Use Neon's branch feature for isolated development environments
- Configure appropriate idle termination settings

## Example Usage
```
-- Python example with asyncpg and connection pooling
import asyncpg
from asyncpg.pool import Pool

async def get_pool() -> Pool:
    return await asyncpg.create_pool(
        "postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/dbname",
        min_size=1,
        max_size=10,
        command_timeout=60,
        # Handle serverless compute startup
        server_settings={
            "application_name": "my-app",
        }
    )

-- Connection handling with retry logic
async def execute_query_with_retry(pool, query, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with pool.acquire() as conn:
                return await conn.fetch(query, *params) if params else await conn.fetch(query)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # exponential backoff
```