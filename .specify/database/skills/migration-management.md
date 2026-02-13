# Migration Management Skill

## Purpose
Perform database migrations safely and effectively in Neon Serverless PostgreSQL.

## Implementation Guidelines
- Use proper migration strategies (additive migrations preferred)
- Always test migrations on a copy of production data
- Include rollback strategies for each migration
- Use transactional migrations when possible
- Follow zero-downtime deployment patterns

## Best Practices
- Use migration tools like Alembic for Python projects
- Always backup data before major migrations
- Test migrations in staging environment first
- Use versioned migration files
- Document migration dependencies and order

## Example Usage
```
-- Migration to add priority column to todos
-- File: 001_add_priority_to_todos.sql

-- Up migration
ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 1;

-- Down migration (rollback)
ALTER TABLE todos DROP COLUMN priority;

-- Migration to add categories table
-- File: 002_create_categories_table.sql

-- Up migration
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#000000',
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Down migration (rollback)
DROP TABLE categories;
```