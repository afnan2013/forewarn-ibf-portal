import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface User {
  id: string
  fullName: string
  email: string
  role: 'user' | 'manager' | 'admin' | 'superadmin'
  createdAt: string
}

interface AuthState {
  // State
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  register: (userData: Omit<User, 'id' | 'createdAt'>, password: string) => Promise<{ success: boolean; error?: string }>
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>
  logout: () => void
  setUser: (user: User) => void
  checkAuth: () => boolean
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isLoading: false,

      // Register action - save user to localStorage
      register: async (userData: Omit<User, 'id' | 'createdAt'>, password: string) => {
        set({ isLoading: true })
        console.log('Registering user with data:', userData);
        try {
          // Check if user already exists
          const existingUsers = JSON.parse(localStorage.getItem('registered-users') || '[]')
          const userExists = existingUsers.find((u: User) => u.email === userData.email)
          
          if (userExists) {
            set({ isLoading: false })
            return { success: false, error: 'User with this email already exists' }
          }
          
          // Create new user
          const newUser: User = {
            id: Date.now().toString(),
            ...userData,
            createdAt: new Date().toISOString()
          }
          console.log('New user created:', newUser);
          // Save to registered users list
          const updatedUsers = [...existingUsers, newUser]
          localStorage.setItem('registered-users', JSON.stringify(updatedUsers))
          console.log('Setting user credentials in localStorage');
          // Also save password for login validation (in real app, this would be hashed)
          const userCredentials = JSON.parse(localStorage.getItem('user-credentials') || '{}')
          userCredentials[userData.email] = { userId: newUser.id, password }
          localStorage.setItem('user-credentials', JSON.stringify(userCredentials))
          
          set({ isLoading: false })
          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          console.log(error)
          return { success: false, error: 'Registration failed. Please try again.' }
        }
      },

      // Login action - check against stored users
      login: async (email: string, password: string) => {
        set({ isLoading: true })
        
        try {
          // Get stored credentials
          const userCredentials = JSON.parse(localStorage.getItem('user-credentials') || '{}')
          const credentials = userCredentials[email]
          
          if (!credentials || credentials.password !== password) {
            set({ isLoading: false })
            return { success: false, error: 'Invalid email or password' }
          }
          
          // Get user data
          const registeredUsers = JSON.parse(localStorage.getItem('registered-users') || '[]')
          const user = registeredUsers.find((u: User) => u.id === credentials.userId)
          
          if (!user) {
            set({ isLoading: false })
            return { success: false, error: 'User not found' }
          }
          
          // Login successful
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false 
          })

          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          console.log('Login Error: ', error)
          return { 
            success: false, 
            error: 'Login failed. Please try again.' 
          }
        }
      },

      // Logout action
      logout: () => {
        set({ 
          user: null, 
          isAuthenticated: false 
        })
        // Clear localStorage
        localStorage.removeItem('auth-storage')
      },

      // Set user (for when we get user from server)
      setUser: (user: User) => {
        set({ user, isAuthenticated: true })
      },

      // Check if user is authenticated
      checkAuth: () => {
        const state = get()
        return state.isAuthenticated && state.user !== null
      },

      // Clear all auth data
      clearAuth: () => {
        set({ user: null, isAuthenticated: false })
      }
    }),
    {
      name: 'auth-storage', // localStorage key
      partialize: (state) => ({ 
        user: state.user, 
        isAuthenticated: state.isAuthenticated 
      })
    }
  )
)
