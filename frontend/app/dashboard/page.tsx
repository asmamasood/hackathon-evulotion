'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { TodoItem } from '../../components/ui/todo-item'
import { TodoForm } from '../../components/ui/todo-form'
import { getUserTodos, createUserTodo, updateUserTodo, deleteUserTodo, toggleTodoComplete } from '../../lib/api'
import { getCurrentUserId } from '../../lib/auth'
import Link from 'next/link'

interface Todo {
  id: string
  title: string
  description?: string
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

export default function Dashboard() {
  const router = useRouter()
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('auth-token')
    if (!token) {
      router.push('/login')
      return
    }
    
    // Load todos from API
    loadTodos()
  }, [router])

  const loadTodos = async () => {
    try {
      setLoading(true)
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found in token')
      }
      const response = await getUserTodos(userId)
      setTodos(response.todos || [])
    } catch (err) {
      setError('Failed to load todos')
      console.error('Load todos error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddTodo = async (title: string, description?: string) => {
    try {
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found in token')
      }
      const response = await createUserTodo(userId, { title, description })
      setTodos([...todos, response])
    } catch (err) {
      setError('Failed to add todo')
      console.error('Add todo error:', err)
    }
  }

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found in token')
      }
      const response = await updateUserTodo(userId, id, updates)
      setTodos(todos.map(todo => 
        todo.id === id ? response : todo
      ))
    } catch (err) {
      setError('Failed to update todo')
      console.error('Update todo error:', err)
    }
  }

  const handleDeleteTodo = async (id: string) => {
    try {
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found in token')
      }
      await deleteUserTodo(userId, id)
      setTodos(todos.filter(todo => todo.id !== id))
    } catch (err) {
      setError('Failed to delete todo')
      console.error('Delete todo error:', err)
    }
  }

  const handleToggleComplete = async (id: string) => {
    try {
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found in token')
      }
      const todo = todos.find(t => t.id === id)
      if (todo) {
        const response = await toggleTodoComplete(userId, id, !todo.completed)
        setTodos(todos.map(todo => 
          todo.id === id ? response : todo
        ))
      }
    } catch (err) {
      setError('Failed to update todo')
      console.error('Toggle complete error:', err)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth-token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 shadow-xl">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="bg-white p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white">Todo Dashboard</h1>
          </div>
          <div className="flex space-x-4">
            <Link 
              href="/chat"
              className="px-6 py-3 bg-white text-indigo-600 rounded-xl hover:bg-gray-100 transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <div className="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
                </svg>
                AI Assistant
              </div>
            </Link>
            <button
              onClick={handleLogout}
              className="px-6 py-3 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <div className="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 0a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L13 5.414V17a1 1 0 11-2 0V5.414L7.707 8.707a1 1 0 01-1.414-1.414l3-3a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Logout
              </div>
            </button>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="rounded-xl bg-red-50 p-4 mb-6 border border-red-200 shadow-md">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div className="mb-10">
          <TodoForm onAddTodo={handleAddTodo} />
        </div>
        
        <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-200">
          <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
            <h2 className="text-lg font-medium text-gray-800">Your Tasks</h2>
            <p className="mt-1 text-sm text-gray-500">Manage your tasks efficiently</p>
          </div>
          <ul className="divide-y divide-gray-200">
            {todos.length === 0 ? (
              <li className="px-6 py-12 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
                <p className="mt-1 text-sm text-gray-500">Get started by adding a new task.</p>
              </li>
            ) : (
              todos.map((todo) => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  onUpdate={handleUpdateTodo}
                  onDelete={handleDeleteTodo}
                  onToggleComplete={handleToggleComplete}
                />
              ))
            )}
          </ul>
        </div>
      </main>
    </div>
  )
}