"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle, Loader2 } from "lucide-react";

export default function AuthWrapper({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem("access_token");
    const user = localStorage.getItem("user");

    // If no token, show proper message before redirecting
    if (!token) {
      setAuthError("No authentication token found. Please log in again.");
      setLoading(false);
      setTimeout(() => {
        router.push("/");
      }, 2000);
      return;
    }

    // If we have both token and user data, assume authenticated
    // This makes the auth less strict and avoids constant API calls
    if (token && user) {
      try {
        const userData = JSON.parse(user);
        if (userData && userData.id) {
          setIsAuthenticated(true);
          setLoading(false);
          return;
        }
      } catch (e) {
        console.log("Invalid user data in localStorage");
      }
    }

    // Only make API call if we have token but no valid user data
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/me/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const userData = await response.json();
        localStorage.setItem("user", JSON.stringify(userData));
        setIsAuthenticated(true);
      } else if (response.status === 401) {
        // Try to refresh token only if we have a refresh token
        const refreshTokenValue = localStorage.getItem("refresh_token");
        if (refreshTokenValue) {
          await refreshToken();
        } else {
          setAuthError("Session expired. Please log in again.");
          setTimeout(() => {
            clearAuthData();
            router.push("/");
          }, 2000);
        }
      } else {
        // For other errors, just proceed with existing data if available
        if (user) {
          setIsAuthenticated(true);
        } else {
          setAuthError("Authentication failed. Please log in again.");
          setTimeout(() => {
            clearAuthData();
            router.push("/");
          }, 2000);
        }
      }
    } catch (error) {
      console.error("Auth check failed:", error);
      // If we have user data, still allow access (less strict)
      if (user) {
        console.log("Using cached user data due to network error");
        setIsAuthenticated(true);
      } else {
        setAuthError(
          "Network error. Please check your connection and try again."
        );
        setTimeout(() => {
          clearAuthData();
          router.push("/");
        }, 3000);
      }
    } finally {
      setLoading(false);
    }
  };

  const clearAuthData = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  };

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem("refresh_token");
    const user = localStorage.getItem("user");

    if (!refreshToken) {
      // If no refresh token but we have user data, allow access (less strict)
      if (user) {
        setIsAuthenticated(true);
        return;
      }
      router.push("/");
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/token/refresh/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh: refreshToken }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access);
        setIsAuthenticated(true);
      } else {
        // If refresh fails but we have user data, still allow access
        if (user) {
          console.log("Token refresh failed, but using cached user data");
          setIsAuthenticated(true);
        } else {
          setAuthError("Session expired. Please log in again.");
          setTimeout(() => {
            clearAuthData();
            router.push("/");
          }, 2000);
        }
      }
    } catch (error) {
      console.error("Token refresh failed:", error);
      // If we have user data, still allow access (less strict)
      if (user) {
        console.log("Using cached user data due to refresh error");
        setIsAuthenticated(true);
      } else {
        setAuthError("Network error. Please try again.");
        setTimeout(() => {
          clearAuthData();
          router.push("/");
        }, 3000);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-600" />
          <p className="mt-4 text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  if (authError) {
    return (
      <div className="flex items-center justify-center min-h-screen p-4">
        <Alert className="max-w-md">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{authError}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return children;
}
