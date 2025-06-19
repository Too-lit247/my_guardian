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
import { Textarea } from "@/components/ui/textarea"
import { Search, Plus, Edit, Trash2, Building, Users, MapPin } from "lucide-react"
import DashboardLayout from "@/components/dashboard-layout"

interface User {
  email: string
  department: string
  role: string
  name: string
  id: string
}

interface District {
  id: string
  name: string
  address: string
  manager: string
  userCount: number
  status: "Active" | "Inactive"
  createdAt: string
  description: string
}

export default function DistrictsPage() {
  const [user, setUser] = useState<User | null>(null)
  const [districts, setDistricts] = useState<District[]>([])
  const [filteredDistricts, setFilteredDistricts] = useState<District[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [isAddDistrictOpen, setIsAddDistrictOpen] = useState(false)
  const [newDistrict, setNewDistrict] = useState({
    name: "",
    address: "",
    manager: "",
    description: "",
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

    // Only regional managers can access this page
    if (currentUser.role !== "regional") {
      router.push("/dashboard")
      return
    }

    // Mock districts data
    const mockDistricts: District[] = [
      {
        id: "1",
        name: "Downtown District",
        address: "123 Main Street, Downtown",
        manager: "John Smith",
        userCount: 15,
        status: "Active",
        createdAt: "2024-01-01T10:00:00Z",
        description: "Central business district covering downtown area",
      },
      {
        id: "2",
        name: "North District",
        address: "456 North Avenue, Northside",
        manager: "Sarah Johnson",
        userCount: 12,
        status: "Active",
        createdAt: "2024-01-05T14:30:00Z",
        description: "Residential and commercial areas in the northern part of the city",
      },
      {
        id: "3",
        name: "South District",
        address: "789 South Boulevard, Southside",
        manager: "Mike Davis",
        userCount: 8,
        status: "Active",
        createdAt: "2024-01-10T09:15:00Z",
        description: "Industrial and residential zones in the southern region",
      },
      {
        id: "4",
        name: "East District",
        address: "321 East Road, Eastside",
        manager: "Emily Brown",
        userCount: 6,
        status: "Inactive",
        createdAt: "2024-01-15T16:45:00Z",
        description: "Suburban areas and new developments in the east",
      },
    ]

    setDistricts(mockDistricts)
    setFilteredDistricts(mockDistricts)
  }, [router])

  useEffect(() => {
    const filtered = districts.filter(
      (district) =>
        district.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        district.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
        district.manager.toLowerCase().includes(searchTerm.toLowerCase()),
    )
    setFilteredDistricts(filtered)
  }, [districts, searchTerm])

  const handleAddDistrict = () => {
    const newDistrictData: District = {
      id: Math.random().toString(36).substr(2, 9),
      name: newDistrict.name,
      address: newDistrict.address,
      manager: newDistrict.manager,
      userCount: 0,
      status: "Active",
      createdAt: new Date().toISOString(),
      description: newDistrict.description,
    }

    setDistricts((prev) => [...prev, newDistrictData])
    setNewDistrict({ name: "", address: "", manager: "", description: "" })
    setIsAddDistrictOpen(false)
  }

  if (!user) return null

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">District Management</h1>
            <p className="text-muted-foreground">
              Manage district branches in your {user.department} department region
            </p>
          </div>
          <Dialog open={isAddDistrictOpen} onOpenChange={setIsAddDistrictOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add District
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>Add New District</DialogTitle>
                <DialogDescription>Create a new district branch for your region</DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="district-name">District Name</Label>
                  <Input
                    id="district-name"
                    value={newDistrict.name}
                    onChange={(e) => setNewDistrict((prev) => ({ ...prev, name: e.target.value }))}
                    placeholder="Enter district name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="district-address">Address</Label>
                  <Input
                    id="district-address"
                    value={newDistrict.address}
                    onChange={(e) => setNewDistrict((prev) => ({ ...prev, address: e.target.value }))}
                    placeholder="Enter district address"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="district-manager">District Manager</Label>
                  <Input
                    id="district-manager"
                    value={newDistrict.manager}
                    onChange={(e) => setNewDistrict((prev) => ({ ...prev, manager: e.target.value }))}
                    placeholder="Enter manager name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="district-description">Description</Label>
                  <Textarea
                    id="district-description"
                    value={newDistrict.description}
                    onChange={(e) => setNewDistrict((prev) => ({ ...prev, description: e.target.value }))}
                    placeholder="Enter district description"
                    rows={3}
                  />
                </div>
                <div className="flex gap-2 pt-4">
                  <Button onClick={handleAddDistrict} className="flex-1">
                    <Building className="h-4 w-4 mr-2" />
                    Add District
                  </Button>
                  <Button variant="outline" onClick={() => setIsAddDistrictOpen(false)}>
                    Cancel
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Districts</CardTitle>
              <Building className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{districts.length}</div>
              <p className="text-xs text-muted-foreground">Active district branches</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Users</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {districts.reduce((sum, district) => sum + district.userCount, 0)}
              </div>
              <p className="text-xs text-muted-foreground">Across all districts</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Districts</CardTitle>
              <MapPin className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{districts.filter((d) => d.status === "Active").length}</div>
              <p className="text-xs text-muted-foreground">Currently operational</p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Search Districts</CardTitle>
            <CardDescription>Find districts by name, address, or manager</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search districts..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Districts ({filteredDistricts.length})</CardTitle>
            <CardDescription>Manage your regional district branches</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>District Name</TableHead>
                    <TableHead>Address</TableHead>
                    <TableHead>Manager</TableHead>
                    <TableHead>Users</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredDistricts.map((district) => (
                    <TableRow key={district.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{district.name}</div>
                          <div className="text-sm text-muted-foreground">{district.description}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">{district.address}</div>
                      </TableCell>
                      <TableCell className="font-medium">{district.manager}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{district.userCount} users</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={district.status === "Active" ? "default" : "secondary"}>
                          {district.status}
                        </Badge>
                      </TableCell>
                      <TableCell>{new Date(district.createdAt).toLocaleDateString()}</TableCell>
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
