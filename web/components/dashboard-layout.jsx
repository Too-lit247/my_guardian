"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter, usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import {
  Home,
  Users,
  Building,
  Bell,
  History,
  Settings,
  LogOut,
  Menu,
  Shield,
  Flame,
  Heart,
  Plus,
  Smartphone,
} from "lucide-react"

export default function DashboardLayout({ children, user }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const router = useRouter()
  const pathname = usePathname()

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token")

      await fetch("http://localhost:8000/api/auth/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user")
      router.push("/")
    }
  }

  const getDepartmentIcon = () => {
    switch (user.department) {
      case "fire":
        return <Flame className="h-5 w-5 text-red-500" />
      case "police":
        return <Shield className="h-5 w-5 text-blue-500" />
      case "medical":
        return <Heart className="h-5 w-5 text-green-500" />
      case "admin":
        return <Shield className="h-5 w-5 text-white" />
      default:
        return null
    }
  }

  const getDepartmentTheme = () => {
    switch (user.department) {
      case "fire":
        return {
          primary: "bg-red-600",
          secondary: "bg-red-50",
          border: "border-red-500",
          text: "text-red-600",
          hover: "hover:bg-red-700",
        }
      case "police":
        return {
          primary: "bg-blue-600",
          secondary: "bg-blue-50",
          border: "border-blue-500",
          text: "text-blue-600",
          hover: "hover:bg-blue-700",
        }
      case "medical":
        return {
          primary: "bg-green-600",
          secondary: "bg-green-50",
          border: "border-green-500",
          text: "text-green-600",
          hover: "hover:bg-green-700",
        }
      case "admin":
        return {
          primary: "bg-gray-900",
          secondary: "bg-gray-50",
          border: "border-gray-800",
          text: "text-gray-900",
          hover: "hover:bg-gray-800",
        }
      default:
        return {
          primary: "bg-gray-600",
          secondary: "bg-gray-50",
          border: "border-gray-500",
          text: "text-gray-600",
          hover: "hover:bg-gray-700",
        }
    }
  }

  const theme = getDepartmentTheme()

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: Home },
    { name: "Alerts", href: "/dashboard/alerts", icon: Bell },
    { name: "History", href: "/dashboard/history", icon: History },
    ...(user.role === "System Administrator"
      ? [
          { name: "Devices", href: "/dashboard/devices", icon: Smartphone },
          { name: "All Users", href: "/dashboard/all-users", icon: Users },
          { name: "Departments", href: "/dashboard/departments", icon: Building },
        ]
      : []),
    ...(user.role === "Regional Manager" ? [{ name: "Districts", href: "/dashboard/districts", icon: Building }] : []),
    ...(user.role === "Regional Manager" || user.role === "District Manager"
      ? [{ name: "Users", href: "/dashboard/users", icon: Users }]
      : []),
  ]

  const Sidebar = () => (
    <div className="flex h-full flex-col">
      <div className={`flex h-16 items-center border-b px-4 ${theme.border} ${theme.primary}`}>
        <div className="flex items-center gap-2">
          {getDepartmentIcon()}
          <div className="text-white">
            <h2 className="font-semibold">My Guardian Plus</h2>
            <p className="text-xs opacity-90">
              {user.role} - {user.full_name}
            </p>
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                isActive
                  ? `${theme.primary} text-white`
                  : `text-muted-foreground hover:${theme.secondary} hover:${theme.text}`
              }`}
              onClick={() => setSidebarOpen(false)}
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </Link>
          )
        })}
      </nav>
      <div className="border-t p-4">
        <Button
          variant="ghost"
          className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50"
          onClick={handleLogout}
        >
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </Button>
      </div>
    </div>
  )

  console.log(localStorage.getItem("user"));
  

  return (
    <div className="flex h-screen bg-background">
      {/* Desktop Sidebar */}
      <div className="hidden w-64 border-r bg-card lg:block">
        <Sidebar />
      </div>

      {/* Mobile Sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetContent side="left" className="w-64 p-0">
          <Sidebar />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className={`flex h-16 items-center border-b bg-card px-4 lg:px-6 ${theme.border}`}>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setSidebarOpen(true)}>
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
          </Sheet>
          <div className="ml-auto flex items-center gap-2">
            <Link href="/dashboard/alerts/new">
              <Button size="sm" className={`${theme.primary} ${theme.hover} text-white`}>
                <Plus className="h-4 w-4 mr-2" />
                New Alert
              </Button>
            </Link>
          </div>
        </header>
        <main className="flex-1 overflow-auto p-4 lg:p-6">{children}</main>
      </div>
    </div>
  )
}
