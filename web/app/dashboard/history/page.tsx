"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Search, Calendar, Clock, MapPin } from "lucide-react"
import DashboardLayout from "@/components/dashboard-layout"

interface User {
  email: string
  department: string
  role: string
  name: string
  id: string
}

interface HistoryRecord {
  id: string
  type: string
  title: string
  location: string
  priority: "High" | "Medium" | "Low"
  status: "Resolved" | "Cancelled"
  createdAt: string
  resolvedAt: string
  assignedTo: string
  responseTime: string
  outcome: string
}

export default function HistoryPage() {
  const [user, setUser] = useState<User | null>(null)
  const [history, setHistory] = useState<HistoryRecord[]>([])
  const [filteredHistory, setFilteredHistory] = useState<HistoryRecord[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [timeFilter, setTimeFilter] = useState("all")
  const router = useRouter()

  useEffect(() => {
    const userData = localStorage.getItem("user")
    if (!userData) {
      router.push("/")
      return
    }
    setUser(JSON.parse(userData))

    // Mock history data
    const mockHistory: HistoryRecord[] = [
      {
        id: "1",
        type: "Fire",
        title: "Apartment Building Fire",
        location: "Oak Street Apartments, Unit 4B",
        priority: "High",
        status: "Resolved",
        createdAt: "2024-01-14T15:30:00Z",
        resolvedAt: "2024-01-14T17:45:00Z",
        assignedTo: "Fire Team Alpha",
        responseTime: "8 minutes",
        outcome: "Fire extinguished, no casualties",
      },
      {
        id: "2",
        type: "Medical",
        title: "Cardiac Emergency",
        location: "Shopping Mall Food Court",
        priority: "High",
        status: "Resolved",
        createdAt: "2024-01-14T12:15:00Z",
        resolvedAt: "2024-01-14T12:45:00Z",
        assignedTo: "Ambulance Unit 2",
        responseTime: "6 minutes",
        outcome: "Patient stabilized and transported to hospital",
      },
      {
        id: "3",
        type: "Police",
        title: "Break-in Report",
        location: "Electronics Store, Main Street",
        priority: "Medium",
        status: "Resolved",
        createdAt: "2024-01-13T22:30:00Z",
        resolvedAt: "2024-01-14T01:15:00Z",
        assignedTo: "Police Unit 5",
        responseTime: "12 minutes",
        outcome: "Suspect apprehended, stolen items recovered",
      },
      {
        id: "4",
        type: "Fire",
        title: "False Alarm - Smoke Detector",
        location: "Office Building, 5th Floor",
        priority: "Low",
        status: "Cancelled",
        createdAt: "2024-01-13T14:20:00Z",
        resolvedAt: "2024-01-13T14:35:00Z",
        assignedTo: "Fire Team Beta",
        responseTime: "5 minutes",
        outcome: "False alarm due to burnt food in break room",
      },
      {
        id: "5",
        type: "Medical",
        title: "Slip and Fall Injury",
        location: "City Park Walking Trail",
        priority: "Medium",
        status: "Resolved",
        createdAt: "2024-01-12T16:45:00Z",
        resolvedAt: "2024-01-12T17:30:00Z",
        assignedTo: "Ambulance Unit 1",
        responseTime: "10 minutes",
        outcome: "Minor injuries treated on scene",
      },
      {
        id: "6",
        type: "Police",
        title: "Domestic Disturbance",
        location: "Residential Area, Pine Street",
        priority: "High",
        status: "Resolved",
        createdAt: "2024-01-11T20:10:00Z",
        resolvedAt: "2024-01-11T21:45:00Z",
        assignedTo: "Police Unit 3",
        responseTime: "7 minutes",
        outcome: "Situation de-escalated, counseling resources provided",
      },
    ]
    setHistory(mockHistory)
    setFilteredHistory(mockHistory)
  }, [router])

  useEffect(() => {
    let filtered = history

    if (searchTerm) {
      filtered = filtered.filter(
        (record) =>
          record.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          record.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
          record.outcome.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter((record) => record.status.toLowerCase() === statusFilter)
    }

    if (timeFilter !== "all") {
      const now = new Date()
      const filterDate = new Date()

      switch (timeFilter) {
        case "today":
          filterDate.setHours(0, 0, 0, 0)
          break
        case "week":
          filterDate.setDate(now.getDate() - 7)
          break
        case "month":
          filterDate.setMonth(now.getMonth() - 1)
          break
      }

      if (timeFilter !== "all") {
        filtered = filtered.filter((record) => new Date(record.createdAt) >= filterDate)
      }
    }

    setFilteredHistory(filtered)
  }, [history, searchTerm, statusFilter, timeFilter])

  if (!user) return null

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "High":
        return "destructive"
      case "Medium":
        return "default"
      case "Low":
        return "secondary"
      default:
        return "secondary"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Resolved":
        return "default"
      case "Cancelled":
        return "secondary"
      default:
        return "secondary"
    }
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Alert History</h1>
          <p className="text-muted-foreground">View past emergency alerts and their outcomes</p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Resolved</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{history.filter((h) => h.status === "Resolved").length}</div>
              <p className="text-xs text-muted-foreground">Successfully handled alerts</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">8.2m</div>
              <p className="text-xs text-muted-foreground">Average time to respond</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <MapPin className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">94%</div>
              <p className="text-xs text-muted-foreground">Successful resolutions</p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Filters</CardTitle>
            <CardDescription>Filter history by search terms, status, or time period</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4 md:flex-row md:items-center">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search history..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full md:w-[180px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="resolved">Resolved</SelectItem>
                  <SelectItem value="cancelled">Cancelled</SelectItem>
                </SelectContent>
              </Select>
              <Select value={timeFilter} onValueChange={setTimeFilter}>
                <SelectTrigger className="w-full md:w-[180px]">
                  <SelectValue placeholder="Filter by time" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Time</SelectItem>
                  <SelectItem value="today">Today</SelectItem>
                  <SelectItem value="week">Past Week</SelectItem>
                  <SelectItem value="month">Past Month</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Alert History ({filteredHistory.length})</CardTitle>
            <CardDescription>Complete record of past emergency alerts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Alert</TableHead>
                    <TableHead>Location</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Response Time</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Outcome</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredHistory.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{record.title}</div>
                          <div className="text-sm text-muted-foreground">{record.type}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">{record.location}</div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getPriorityColor(record.priority) as any}>{record.priority}</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusColor(record.status) as any}>{record.status}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm font-medium">{record.responseTime}</div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">{new Date(record.createdAt).toLocaleDateString()}</div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm max-w-xs truncate" title={record.outcome}>
                          {record.outcome}
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
