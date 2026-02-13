# Auth Skills Index

## Overview
This directory contains specialized skills for implementing secure authentication systems. Each skill addresses a specific aspect of authentication and authorization.

## Available Skills

### 1. Password Hashing (`password-hashing.md`)
Securely hash and verify passwords using industry-standard algorithms.

### 2. JWT Token Management (`jwt-management.md`)
Handle JWT token creation, validation, refresh, and revocation.

### 3. Session Management (`session-management.md`)
Manage secure user sessions with proper security controls.

### 4. OAuth Integration (`oauth-integration.md`)
Integrate third-party OAuth providers securely.

## Best Practices
- Always follow the principle of least privilege
- Implement defense in depth security measures
- Regularly audit authentication code for vulnerabilities
- Keep dependencies updated to address security patches
- Log authentication events for security monitoring
- Use environment variables for all secrets and configuration

## Integration Guidelines
- Each skill can be implemented independently
- Skills should work together to form a complete auth system
- Follow consistent error handling across all skills
- Maintain detailed documentation for each implementation
- Include comprehensive tests for all authentication flows