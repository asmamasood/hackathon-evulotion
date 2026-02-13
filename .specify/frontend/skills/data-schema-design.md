# Data Schema Design Skill

## Purpose
Design table migration schemas and data structures for frontend-backend integration.

## Implementation Guidelines
- Create clear data models that align with frontend requirements
- Design efficient data structures for optimal frontend performance
- Plan database migrations that support frontend features
- Document API endpoints that correspond to data models
- Consider pagination and filtering requirements

## Best Practices
- Normalize data structures to reduce redundancy
- Plan for scalability and performance
- Design flexible schemas that accommodate future changes
- Document relationships between different data entities
- Consider caching strategies for improved performance

## Example Usage
```
// Example User schema for a Todo app
{
  id: UUID,
  name: String,
  email: String,
  created_at: DateTime,
  updated_at: DateTime
}

// Example Todo schema
{
  id: UUID,
  title: String,
  description: Text,
  completed: Boolean,
  user_id: UUID (foreign key),
  created_at: DateTime,
  updated_at: DateTime
}

// Corresponding API endpoints
GET /api/users/:id/todos
POST /api/todos
PUT /api/todos/:id
DELETE /api/todos/:id
```