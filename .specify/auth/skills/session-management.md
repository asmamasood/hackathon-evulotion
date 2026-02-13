# Session Management Skill

## Purpose
Handle secure session creation, maintenance, and destruction.

## Implementation Guidelines
- Use secure, HttpOnly cookies for session tokens
- Set SameSite attribute to prevent CSRF attacks
- Implement automatic session expiration
- Store session data securely (server-side or signed client-side)
- Regenerate session IDs after login to prevent session fixation

## Security Considerations
- Encrypt sensitive session data
- Implement concurrent session limits
- Track session activity and detect anomalies
- Securely destroy sessions on logout

## Example Usage
```
// Create new session after successful authentication
const sessionId = await createSession(userId);

// Validate active session
const isValid = await validateSession(sessionId);

// Destroy session on logout
await destroySession(sessionId);
```