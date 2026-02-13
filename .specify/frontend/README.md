# Frontend Agent for Hackathon-2-Todo

## Overview
The Frontend Agent is a specialized component focused on Next.js frontend development for the Hackathon-2-Todo project. It builds responsive, scalable, and well-structured applications using Next.js App Router following modern UI/UX best practices.

## Features
- Next.js App Router implementation
- Responsive UI design across all device sizes
- Data schema design for frontend-backend integration
- Component architecture and modular design
- Performance optimization
- Accessibility compliance

## Components

### Frontend Agent
Located at: `.specify/frontend/frontend-agent.ps1`

The main entry point for frontend-related tasks. Use this script to:
- Display frontend agent information
- List available frontend skills
- Show recommended Next.js project structure

### Frontend Skills
Located at: `.specify/frontend/skills/`

Modular skill sets for different frontend aspects:
- `nextjs-app-router.md` - Next.js App Router implementation
- `responsive-design.md` - Responsive UI design
- `data-schema-design.md` - Data schema design for integration
- `component-architecture.md` - Component architecture patterns

## Usage

### PowerShell
```powershell
# Show frontend agent info and skills
.\.specify\frontend\frontend-agent.ps1

# List available skills
.\.specify\frontend\frontend-agent.ps1 -Command skills

# Show recommended Next.js structure
.\.specify\frontend\frontend-agent.ps1 -Command structure
```

### From the Frontend Agent
The frontend agent can be invoked directly to handle frontend-related tasks following Next.js best practices.

## Integration
This frontend agent integrates with:
- The backend agent for API integration
- Database schemas through data design
- Authentication systems for protected routes

## Best Practices
- Follow Next.js App Router conventions
- Implement responsive design from the start
- Use TypeScript for type safety
- Follow accessibility standards
- Optimize for performance and user experience

## Maintenance
- Regular updates to follow Next.js best practices
- Responsive design testing across devices
- Performance optimization as needed
- Accessibility compliance checks