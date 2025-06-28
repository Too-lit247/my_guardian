"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Shield, Flame, Heart, AlertCircle, UserPlus } from "lucide-react"
import { useRouter } from "next/navigation"

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState("login")
  const [loginData, setLoginData] = useState({
    username: "admin",
    password: "admin123",
    department: "admin",
    role: "System Administrator",
  })
  const [registerData, setRegisterData] = useState({
    full_name: "",
    email: "",
    username: "",
    password: "",
    phone_number: "",
    department: "",
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const router = useRouter()

  const handleLogin = async () => {
    setLoading(true)
    setError("")

    console.log("Attempting login with:", loginData)

    try {
      const response = await fetch("http://localhost:8000/api/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginData),
      })

      console.log("Response status:", response.status)
      console.log("Response headers:", response.headers)

      const data = await response.json()
      console.log("Response data:", data)

      if (response.ok) {
        localStorage.setItem("access_token", data.access)
        localStorage.setItem("refresh_token", data.refresh)
        localStorage.setItem("user", JSON.stringify(data.user))
        router.push("/dashboard")
      } else {
        setError(data.detail || data.non_field_errors?.[0] || "Login failed")
      }
    } catch (err) {
      console.error("Login error:", err)
      setError("Network error. Please check if the backend server is running.")
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async () => {
    setLoading(true)
    setError("")

    try {
      const response = await fetch("http://localhost:8000/api/auth/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(registerData),
      })

      const data = await response.json()

      if (response.ok) {
        setActiveTab("login")
        setError("")
        alert("Registration successful! Your account is pending admin approval. You will be notified when activated.")
      } else {
        setError(data.detail || data.non_field_errors?.[0] || "Registration failed")
      }
    } catch (err) {
      setError("Network error. Please check if the backend server is running.")
    } finally {
      setLoading(false)
    }
  }

  const getDepartmentIcon = (dept) => {
    switch (dept) {
      case "fire":
        return <Flame className="h-5 w-5 text-red-500" />
      case "police":
        return <Shield className="h-5 w-5 text-blue-500" />
      case "medical":
        return <Heart className="h-5 w-5 text-green-500" />
      case "admin":
        return <Shield className="h-5 w-5 text-gray-800" />
      default:
        return null
    }
  }
/*
  const loadSampleCredentials = (type) => {
    const credentials = {
      admin: {
        username: "admin",
        password: "admin123",
        department: "admin",
        role: "System Administrator",
      },
      fire: {
        username: "fire_regional_mw",
        password: "admin123",
        department: "fire",
        role: "Regional Manager",
      },
      police: {
        username: "police_regional_mw",
        password: "admin123",
        department: "police",
        role: "Regional Manager",
      },
      medical: {
        username: "medical_regional_mw",
        password: "admin123",
        department: "medical",
        role: "Regional Manager",
      },
    }
    setLoginData(credentials[type])
  }
*/
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">My Guardian Plus</CardTitle>
          <CardDescription>Emergency Response Management System</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="register">Register</TabsTrigger>
            </TabsList>

            <TabsContent value="login" className="space-y-4">
              {error && (
                <div className="flex items-center gap-2 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded">
                  <AlertCircle className="h-4 w-4" />
                  {error}
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  value={loginData.username}
                  onChange={(e) => setLoginData((prev) => ({ ...prev, username: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={loginData.password}
                  onChange={(e) => setLoginData((prev) => ({ ...prev, password: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="department">Department</Label>
                <Select
                  value={loginData.department}
                  onValueChange={(value) => setLoginData((prev) => ({ ...prev, department: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select your department" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fire">
                      <div className="flex items-center gap-2">
                        <Flame className="h-4 w-4 text-red-500" />
                        Fire Department
                      </div>
                    </SelectItem>
                    <SelectItem value="police">
                      <div className="flex items-center gap-2">
                        <Shield className="h-4 w-4 text-blue-500" />
                        Police Department
                      </div>
                    </SelectItem>
                    <SelectItem value="medical">
                      <div className="flex items-center gap-2">
                        <Heart className="h-4 w-4 text-green-500" />
                        Medical Department
                      </div>
                    </SelectItem>
                    <SelectItem value="admin">
                      <div className="flex items-center gap-2">
                        <Shield className="h-4 w-4 text-gray-800" />
                        System Administrator
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <Select
                  value={loginData.role}
                  onValueChange={(value) => setLoginData((prev) => ({ ...prev, role: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select your role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="System Administrator">System Administrator</SelectItem>
                    <SelectItem value="Regional Manager">Regional Manager</SelectItem>
                    <SelectItem value="District Manager">District Manager</SelectItem>
                    <SelectItem value="Field User">Field User</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                className="w-full"
                onClick={handleLogin}
                disabled={
                  !loginData.username || !loginData.password || !loginData.department || !loginData.role || loading
                }
              >
                {loading ? "Signing In..." : "Sign In"}
              </Button>

              {/* <div className="text-center text-sm text-muted-foreground space-y-2">
                <p className="font-medium">Quick Login Options:</p>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("admin")}>
                    Admin
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("fire")}>
                    Fire Dept
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("police")}>
                    Police
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("medical")}>
                    Medical
                  </Button>
                </div>
                <p className="text-xs mt-2">
                  Default password for all accounts: <code>admin123</code>
                </p>
              </div> */}
            </TabsContent>

            <TabsContent value="register" className="space-y-4">
              {error && (
                <div className="flex items-center gap-2 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded">
                  <AlertCircle className="h-4 w-4" />
                  {error}
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="full_name">Full Name</Label>
                <Input
                  id="full_name"
                  placeholder="Enter your full name"
                  value={registerData.full_name}
                  onChange={(e) => setRegisterData((prev) => ({ ...prev, full_name: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={registerData.email}
                  onChange={(e) => setRegisterData((prev) => ({ ...prev, email: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="reg_username">Username</Label>
                <Input
                  id="reg_username"
                  placeholder="Choose a username"
                  value={registerData.username}
                  onChange={(e) => setRegisterData((prev) => ({ ...prev, username: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="reg_password">Password</Label>
                <Input
                  id="reg_password"
                  type="password"
                  placeholder="Choose a password"
                  value={registerData.password}
                  onChange={(e) => setRegisterData((prev) => ({ ...prev, password: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  placeholder="Enter your phone number"
                  value={registerData.phone_number}
                  onChange={(e) => setRegisterData((prev) => ({ ...prev, phone_number: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="reg_department">Department</Label>
                <Select
                  value={registerData.department}
                  onValueChange={(value) => setRegisterData((prev) => ({ ...prev, department: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select department" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fire">Fire Department</SelectItem>
                    <SelectItem value="police">Police Department</SelectItem>
                    <SelectItem value="medical">Medical Department</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                className="w-full"
                onClick={handleRegister}
                disabled={
                  !registerData.full_name ||
                  !registerData.email ||
                  !registerData.username ||
                  !registerData.password ||
                  !registerData.department ||
                  loading
                }
              >
                <UserPlus className="h-4 w-4 mr-2" />
                {loading ? "Registering..." : "Register"}
              </Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

