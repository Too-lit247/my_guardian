"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, Plus, Edit, Trash2, UserPlus } from "lucide-react"
import DashboardLayout from "@/components/dashboard-layout"

interface User {
  email: string
  department: string
  role: string
  name: string
  id: string
}

interface SystemUser {
  id: string
  name: string
  email: string
  role: string
  department: string
  district: string
  status: "Active" | "Inactive"
  createdAt: string
}

export default function UsersPage() {
  const [user, setUser] = useState<User | null>(null)
  const [users, setUsers] = useState<SystemUser[]>([])
  const [filteredUsers, setFilteredUsers] = useState<SystemUser[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [isAddUserOpen, setIsAddUserOpen] = useState(false)
  const [newUser, setNewUser] = useState({
    name: "",
    email: "",
    role: "",
    district: "",
  })
  const router = useRouter()

  useEffect(() => {
    const userData = localStorage.getItem("user")
    if (!userData) {
      router.push("/")
      return
    }
    const currentUser = JSON.parse(userData)
    setUser(currentUser)

    // Mock users data
    const mockUsers: SystemUser[] = [
      {
        id: "1",
        name: "John Smith",
        email: "john.smith@fire.gov",
        role: "district",
        department: "fire",
        district: "Downtown District",
        status: "Active",
        createdAt: "2024-01-10T10:00:00Z",
      },
      {
        id: "2",
        name: "Sarah Johnson",
        email: "sarah.johnson@fire.gov",
        role: "user",
        department: "fire",
        district: "Downtown District",
        status: "Active",
        createdAt: "2024-01-12T14:30:00Z",
      },
      {
        id: "3",
        name: "Mike Davis",
        email: "mike.davis@police.gov",
        role: "district",
        department: "police",
        district: "North District",
        status: "Active",
        createdAt: "2024-01-08T09:15:00Z",
      },
      {
        id: "4",
        name: "Emily Brown",
        email: "emily.brown@medical.gov",
        role: "user",
        department: "medical",
        district: "Central District",
        status: "Inactive",
        createdAt: "2024-01-05T16:45:00Z",
      },
    ]

    // Filter users based on current user's role and department
    let filteredMockUsers = mockUsers
    if (currentUser.role === "district") {
      filteredMockUsers = mockUsers.filter((u) => u.department === currentUser.department && u.role === "user")
    } else if (currentUser.role === "regional") {
      filteredMockUsers = mockUsers.filter((u) => u.department === currentUser.department)
    }

    setUsers(filteredMockUsers)
    setFilteredUsers(filteredMockUsers)
  }, [router])

  useEffect(() => {
    const filtered = users.filter(
      (user) =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.district.toLowerCase().includes(searchTerm.toLowerCase()),
    )
    setFilteredUsers(filtered)
  }, [users, searchTerm])

  const handleAddUser = () => {
    const newSystemUser: SystemUser = {
      id: Math.random().toString(36).substr(2, 9),
      name: newUser.name,
      email: newUser.email,
      role: newUser.role,
      department: user?.department || "",
      district: newUser.district,
      status: "Active",
      createdAt: new Date().toISOString(),
    }

    setUsers((prev) => [...prev, newSystemUser])
    setNewUser({ name: "", email: "", role: "", district: "" })
    setIsAddUserOpen(false)
  }

  if (!user) return null

  const canAddUsers = user.role === "regional" || user.role === "district"

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">User Management</h1>
            <p className="text-muted-foreground">
              Manage users in your {user.role === "regional" ? "region" : "district"}
            </p>
          </div>
          {canAddUsers && (
            <Dialog open={isAddUserOpen} onOpenChange={setIsAddUserOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Add User
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New User</DialogTitle>
                  <DialogDescription>Create a new user account for your {user.department} department</DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      value={newUser.name}
                      onChange={(e) => setNewUser((prev) => ({ ...prev, name: e.target.value }))}
                      placeholder="Enter full name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={newUser.email}
                      onChange={(e) => setNewUser((prev) => ({ ...prev, email: e.target.value }))}
                      placeholder="Enter email address"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="role">Role</Label>
                    <Select
                      value={newUser.role}
                      onValueChange={(value) => setNewUser((prev) => ({ ...prev, role: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select role" />
                      </SelectTrigger>
                      <SelectContent>
                        {user.role === "regional" && <SelectItem value="district">District Manager</SelectItem>}
                        <SelectItem value="user">Field User</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="district">District</Label>
                    <Select
                      value={newUser.district}
                      onValueChange={(value) => setNewUser((prev) => ({ ...prev, district: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select district" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Downtown District">Downtown District</SelectItem>
                        <SelectItem value="North District">North District</SelectItem>
                        <SelectItem value="South District">South District</SelectItem>
                        <SelectItem value="East District">East District</SelectItem>
                        <SelectItem value="West District">West District</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="flex gap-2 pt-4">
                    <Button onClick={handleAddUser} className="flex-1">
                      <UserPlus className="h-4 w-4 mr-2" />
                      Add User
                    </Button>
                    <Button variant="outline" onClick={() => setIsAddUserOpen(false)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          )}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Search Users</CardTitle>
            <CardDescription>Find users by name, email, or district</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search users..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Users ({filteredUsers.length})</CardTitle>
            <CardDescription>Manage users in your department</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>District</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map((systemUser) => (
                    <TableRow key={systemUser.id}>
                      <TableCell className="font-medium">{systemUser.name}</TableCell>
                      <TableCell>{systemUser.email}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="capitalize">
                          {systemUser.role}
                        </Badge>
                      </TableCell>
                      <TableCell>{systemUser.district}</TableCell>
                      <TableCell>
                        <Badge variant={systemUser.status === "Active" ? "default" : "secondary"}>
                          {systemUser.status}
                        </Badge>
                      </TableCell>
                      <TableCell>{new Date(systemUser.createdAt).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
