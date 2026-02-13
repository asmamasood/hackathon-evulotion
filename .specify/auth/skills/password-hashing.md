# Password Hashing Skill

## Purpose
Securely hash passwords using industry-standard algorithms like bcrypt or argon2.

## Implementation Guidelines
- Use bcrypt with a minimum cost factor of 12 or argon2 with recommended parameters
- Never store plain text passwords
- Always salt passwords during hashing
- Compare passwords using constant-time comparison functions

## Security Considerations
- Store only the hashed password, never the original
- Use environment variables for any hashing parameters
- Regularly update hashing algorithms as security evolves

## Example Usage
```
// When registering a user
const hashedPassword = await hashPassword(userInputPassword);

// When verifying login
const isValid = await verifyPassword(inputPassword, storedHash);
```