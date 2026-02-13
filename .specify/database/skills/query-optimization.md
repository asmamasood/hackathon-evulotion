# Query Optimization Skill

## Purpose
Optimize queries and indexes for performance in Neon Serverless PostgreSQL.

## Implementation Guidelines
- Analyze query execution plans using EXPLAIN ANALYZE
- Create appropriate indexes for frequently queried columns
- Avoid SELECT * statements, specify only needed columns
- Use parameterized queries to prevent SQL injection
- Implement proper pagination for large datasets

## Best Practices
- Monitor slow query logs regularly
- Use composite indexes for multi-column queries
- Consider partial indexes for filtered queries
- Implement read replicas for read-heavy workloads
- Use connection pooling for better resource utilization

## Example Usage
```
-- Slow query (without proper indexing)
SELECT * FROM todos WHERE user_id = $1 AND completed = true;

-- Optimized with proper indexing
CREATE INDEX idx_todos_user_id_completed ON todos(user_id, completed);

-- Efficient pagination
SELECT * FROM todos 
WHERE user_id = $1 
ORDER BY created_at DESC 
LIMIT $2 OFFSET $3;

-- Using EXPLAIN to analyze query performance
EXPLAIN ANALYZE 
SELECT t.*, u.username 
FROM todos t 
JOIN users u ON t.user_id = u.id 
WHERE t.completed = false;
```