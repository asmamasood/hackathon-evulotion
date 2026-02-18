/**
 * Authentication utility functions for the Todo application
 */

/**
 * Checks if the user is authenticated
 */
export function isAuthenticated(): boolean {
  const token = localStorage.getItem('auth-token')
  return !!token
}

/**
 * Gets the current user's token
 */
export function getToken(): string | null {
  return localStorage.getItem('auth-token')
}

/**
 * Sets the user's token
 */
export function setToken(token: string): void {
  localStorage.setItem('auth-token', token)
}

/**
 * Removes the user's token (logout)
 */
export function removeToken(): void {
  localStorage.removeItem('auth-token')
}

/**
 * Decodes a JWT token to extract the payload
 */
export function decodeToken(token: string): any {
  try {
    // Split the token to get the payload part (middle part of JWT)
    const parts = token.split('.')
    if (parts.length !== 3) {
      throw new Error('Invalid token format')
    }
    
    // Decode the payload (second part)
    const payload = parts[1]
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4)
    const decodedPayload = atob(paddedPayload)
    return JSON.parse(decodedPayload)
  } catch (error) {
    console.error('Error decoding token:', error)
    return null
  }
}

/**
 * Gets the current user's ID from the token
 */
export function getCurrentUserId(): string | null {
  const token = getToken()
  if (!token) {
    return null
  }
  
  const decoded = decodeToken(token)
  return decoded?.sub || null  // 'sub' is the standard claim for subject/user ID in JWT
}