# Schema Design Skill

## Purpose
Design database schemas for scalability and maintainability in Neon Serverless PostgreSQL.

## Implementation Guidelines
- Use proper normalization techniques (typically 3NF)
- Design for scalability with appropriate partitioning when needed
- Plan for future growth and schema evolution
- Use appropriate data types for efficiency
- Design clear relationships between tables

## Best Practices
- Use consistent naming conventions (snake_case for PostgreSQL)
- Implement proper primary and foreign key constraints
- Design for data integrity with appropriate constraints
- Plan for indexing strategies from the beginning
- Document schema decisions and relationships

## Example Usage
```
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
```