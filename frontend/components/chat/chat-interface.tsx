'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { sendMessage } from '../../lib/api'
import { getCurrentUserId } from '../../lib/auth'

interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
}

export default function ChatInterface() {
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. You can ask me to add, list, update, complete, or delete tasks.',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('auth-token')
    if (!token) {
      router.push('/login')
      return
    }
  }, [router])

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    try {
      setIsLoading(true)
      
      // Add user message to UI immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: inputText,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, userMessage])
      const userInput = inputText
      setInputText('')
      
      // Send message to backend
      const userId = getCurrentUserId()
      if (!userId) {
        throw new Error('User ID not found')
      }
      
      const response = await sendMessage(userInput)
      
      // Add AI response to UI
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Add error message to UI
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth-token')
    router.push('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex flex-col">
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="bg-white p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white">AI Todo Assistant</h1>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-white text-indigo-600 rounded-lg hover:bg-gray-100 transition-all duration-200 font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
          >
            Logout
          </button>
        </div>
      </header>
      
      <main className="flex-1 flex flex-col max-w-4xl w-full mx-auto m-4">
        <div className="bg-white rounded-xl shadow-xl overflow-hidden flex flex-col h-[calc(100vh-200px)]">
          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-gray-50 to-gray-100" style={{ maxHeight: 'calc(100vh - 250px)' }}>
            <div className="space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-5 py-3 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-br-none'
                        : 'bg-white text-gray-800 rounded-bl-none shadow-md border border-gray-200'
                    }`}
                  >
                    <div className="whitespace-pre-wrap break-words">{message.content}</div>
                    <div className={`text-xs mt-2 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-[85%] rounded-2xl px-5 py-3 bg-white text-gray-800 rounded-bl-none shadow-md border border-gray-200">
                    <div className="flex items-center">
                      <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce mr-1"></div>
                      <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce mr-1 delay-75"></div>
                      <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce delay-150"></div>
                      <span className="ml-2">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
          
          {/* Input Area */}
          <div className="border-t border-gray-200 p-5 bg-white">
            <div className="flex items-end space-x-3">
              <div className="flex-1 bg-gray-100 rounded-xl p-1">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask me to add, list, update, complete, or delete tasks..."
                  className="w-full bg-transparent border-0 focus:ring-0 focus:outline-none resize-none py-3 px-4 text-gray-700 placeholder-gray-500"
                  rows={2}
                  disabled={isLoading}
                />
              </div>
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputText.trim()}
                className={`px-6 py-3 rounded-xl font-medium text-white shadow-lg transition-all duration-200 ${
                  isLoading || !inputText.trim()
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 active:scale-95'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            <div className="mt-3 text-sm text-gray-500 flex justify-between">
              <span>Examples: "Add a task to buy groceries", "Show me my tasks", "Mark task #1 as complete"</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}