# OAuth Integration Skill

## Purpose
Integrate third-party OAuth providers (Google, GitHub, etc.) securely.

## Implementation Guidelines
- Use PKCE (Proof Key for Code Exchange) for public clients
- Validate OAuth state parameters to prevent CSRF
- Properly configure redirect URIs
- Map OAuth provider data to internal user accounts
- Handle OAuth token refresh automatically

## Security Considerations
- Never trust OAuth provider data without validation
- Implement proper account linking/unlinking
- Protect against account hijacking during registration
- Securely store OAuth tokens with limited scope

## Example Usage
```
// Initiate OAuth flow
const authUrl = await initiateOAuth(provider, redirectUri);

// Handle OAuth callback
const userData = await handleOAuthCallback(code, state);

// Link OAuth account to existing user
await linkOAuthAccount(userId, provider, providerUserId);
```