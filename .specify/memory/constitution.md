# Hackathon-2-Todo Constitution

## Core Principles

### I. Library-First
Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries

### II. CLI Interface
Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced

### IV. Integration Testing
Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas

### V. Security-First Approach
All implementations must prioritize security from the ground up; Authentication and authorization handled by dedicated auth agents; Follow OWASP security standards

### VI. Modularity and Separation of Concerns
Different functionality should be separated into distinct modules; Authentication logic isolated in dedicated auth module; Clear interfaces between components

## Security Requirements
Authentication and authorization must follow industry best practices:
- Use secure password hashing (bcrypt/argon2)
- Implement proper JWT token management
- Follow secure session management practices
- Integrate OAuth providers securely
- Protect against common vulnerabilities (XSS, CSRF, injection attacks)

## Development Workflow
- Use dedicated auth agents for authentication-related tasks
- Use dedicated backend agents for FastAPI development
- Use dedicated frontend agents for Next.js development
- Use dedicated database agents for Neon PostgreSQL management
- Follow established patterns and skills across all agents
- Implement comprehensive security testing
- Conduct security reviews for all changes
- Document security decisions and trade-offs

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan

All PRs/reviews must verify compliance; Complexity must be justified; Use agent guidelines for development

**Version**: 1.0.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-13
