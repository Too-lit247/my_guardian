"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export default function AuthWrapper({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem("access_token")

    if (!token) {
      router.push("/")
      return
    }

    try {
      const response = await fetch("http://localhost:8000/api/auth/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        setIsAuthenticated(true)
      } else if (response.status === 401) {
        // Try to refresh token
        await refreshToken()
      } else {
        throw new Error("Authentication failed")
      }
    } catch (error) {
      console.error("Auth check failed:", error)
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user")
      router.push("/")
    } finally {
      setLoading(false)
    }
  }

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem("refresh_token")

    if (!refreshToken) {
      router.push("/")
      return
    }

    try {
      const response = await fetch("http://localhost:8000/api/auth/token/refresh/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh: refreshToken }),
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem("access_token", data.access)
        setIsAuthenticated(true)
      } else {
        throw new Error("Token refresh failed")
      }
    } catch (error) {
      console.error("Token refresh failed:", error)
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user")
      router.push("/")
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return children
}
