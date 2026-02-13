# Database Agent for Hackathon-2-Todo

## Overview
The Database Agent is a specialized component focused on Neon Serverless PostgreSQL management for the Hackathon-2-Todo project. It handles schema design, migrations, query optimization, and Neon-specific integration following PostgreSQL best practices.

## Features
- Schema design for scalability and maintainability
- Safe and effective migration management
- Query optimization and indexing
- Neon Serverless PostgreSQL integration
- Performance tuning and monitoring
- Data integrity and security

## Components

### Database Agent
Located at: `.specify/database/database-agent.ps1`

The main entry point for database-related tasks. Use this script to:
- Display database agent information
- List available database skills
- Show recommended Neon PostgreSQL project structure

### Database Skills
Located at: `.specify/database/skills/`

Modular skill sets for different database aspects:
- `schema-design.md` - Database schema design for scalability
- `migration-management.md` - Safe migration strategies
- `query-optimization.md` - Query performance optimization
- `neon-integration.md` - Neon Serverless integration

## Usage

### PowerShell
```powershell
# Show database agent info and skills
.\.specify\database\database-agent.ps1

# List available skills
.\.specify\database\database-agent.ps1 -Command skills

# Show recommended Neon PostgreSQL structure
.\.specify\database\database-agent.ps1 -Command structure
```

### From the Database Agent
The database agent can be invoked directly to handle database-related tasks following PostgreSQL and Neon best practices.

## Integration
This database agent integrates with:
- The backend agent for API integration
- Application data models
- Authentication system for user data management

## Best Practices
- Follow PostgreSQL and Neon Serverless conventions
- Implement proper data validation and constraints
- Use appropriate indexing strategies for performance
- Include comprehensive backup and recovery procedures
- Monitor query performance regularly

## Maintenance
- Regular updates to follow PostgreSQL best practices
- Performance optimization as needed
- Security audits for database operations
- Migration testing in staging environments