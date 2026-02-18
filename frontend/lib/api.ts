/**
 * API utility functions for the Todo application
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'

interface ApiOptions {
  method?: string
  headers?: Record<string, string>
  body?: any
}

/**
 * Makes an API request with proper authentication
 */
export async function apiRequest(
  endpoint: string,
  options: ApiOptions = {}
): Promise<any> {
  const token = localStorage.getItem('auth-token')
  
  const config: RequestInit = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  }

  if (options.body) {
    config.body = JSON.stringify(options.body)
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error)
    throw error
  }
}

/**
 * Makes an API request without authentication (for login/register)
 */
export async function apiRequestNoAuth(
  endpoint: string,
  options: ApiOptions = {}
): Promise<any> {
  const config: RequestInit = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  }

  if (options.body) {
    config.body = JSON.stringify(options.body)
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error)
    throw error
  }
}

/**
 * Registers a new user
 */
export async function registerUser(userData: { username: string; email: string; password: string }) {
  return apiRequestNoAuth('/users/register', {
    method: 'POST',
    body: userData
  })
}

/**
 * Logs in a user
 */
export async function loginUser(credentials: { email: string; password: string }) {
  return apiRequestNoAuth('/users/login', {
    method: 'POST',
    body: credentials
  })
}

/**
 * Gets all todos for a user
 */
export async function getUserTodos(userId: string) {
  return apiRequest(`/${userId}/todos`)
}

/**
 * Creates a new todo for a user
 */
export async function createUserTodo(userId: string, todoData: { title: string; description?: string }) {
  return apiRequest(`/${userId}/todos`, {
    method: 'POST',
    body: todoData
  })
}

/**
 * Updates a specific todo
 */
export async function updateUserTodo(userId: string, todoId: string, todoData: { title?: string; description?: string }) {
  return apiRequest(`/${userId}/todos/${todoId}`, {
    method: 'PUT',
    body: todoData
  })
}

/**
 * Deletes a specific todo
 */
export async function deleteUserTodo(userId: string, todoId: string) {
  return apiRequest(`/${userId}/todos/${todoId}`, {
    method: 'DELETE'
  })
}

/**
 * Toggles the completion status of a specific todo
 */
export async function toggleTodoComplete(userId: string, todoId: string, completed: boolean) {
  return apiRequest(`/${userId}/todos/${todoId}/complete`, {
    method: 'PATCH',
    body: { completed }
  })
}

/**
 * Sends a message to the AI chatbot
 */
export async function sendMessage(message: string) {
  return apiRequest('/chat', {
    method: 'POST',
    body: { message }
  })
}