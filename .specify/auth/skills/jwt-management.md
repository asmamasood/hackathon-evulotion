# JWT Token Management Skill

## Purpose
Generate, sign, verify, and refresh JWT tokens for secure authentication.

## Implementation Guidelines
- Use strong signing keys stored in environment variables
- Set appropriate expiration times (short-lived access tokens, longer refresh tokens)
- Implement token refresh mechanisms
- Include proper claims (user ID, roles, expiration)
- Sign tokens using HS256 or RS256 algorithm

## Security Considerations
- Never store sensitive information in JWT payloads
- Implement token blacklisting for logout functionality
- Use HTTPS in production environments
- Rotate signing keys periodically

## Example Usage
```
// Generate access and refresh tokens
const { accessToken, refreshToken } = await generateTokens(userId, roles);

// Verify token validity
const payload = await verifyToken(token);

// Refresh expired access token
const newAccessToken = await refreshAccessToken(refreshToken);
```