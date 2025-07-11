"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Users,
  UserCheck,
  UserX,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Building,
  Shield,
  Flame,
  Heart,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";

interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  phone_number: string;
  employee_id: string;
  department: string;
  department_display: string;
  role: string;
  role_display: string;
  district_id: string | null;
  district_name: string | null;
  badge_number: string;
  rank: string;
  years_of_service: number;
  certifications: string;
  is_active: boolean;
  is_active_user: boolean;
  date_joined: string;
  last_login: string | null;
  created_at: string;
  updated_at: string;
}

interface DepartmentRegistration {
  registration_id: string;
  department_name: string;
  department_type: string;
  registration_number: string;
  contact_person: string;
  contact_email: string;
  contact_phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
  coverage_description: string;
  population_served: number;
  regional_manager_name: string;
  regional_manager_email: string;
  regional_manager_phone: string;
  regional_manager_credentials: string;
  status: "pending" | "approved" | "rejected" | "suspended";
  review_notes: string;
  submitted_at: string;
}

export default function AllUsersPage() {
  const [user, setUser] = useState<any | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [registrations, setRegistrations] = useState<DepartmentRegistration[]>(
    []
  );
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("all");
  const [roleFilter, setRoleFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("users");
  const [selectedRegistration, setSelectedRegistration] =
    useState<DepartmentRegistration | null>(null);
  const [isRegistrationDetailsOpen, setIsRegistrationDetailsOpen] =
    useState(false);
  const [isCreateUserOpen, setIsCreateUserOpen] = useState(false);
  const [newUser, setNewUser] = useState({
    username: "",
    email: "",
    full_name: "",
    phone_number: "",
    employee_id: "",
    password: "",
    password_confirm: "",
    department: "",
    role: "",
    district_id: "",
    badge_number: "",
    rank: "",
    years_of_service: 0,
    certifications: "",
  });
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      router.push("/");
      return;
    }
    const currentUser = JSON.parse(userData);
    setUser(currentUser);

    // Only system administrators can access this page
    if (currentUser.role !== "System Administrator") {
      router.push("/dashboard");
      return;
    }

    fetchUsers();
    fetchDepartmentRegistrations();
  }, [router]);

  useEffect(() => {
    let filtered = users;

    if (searchTerm) {
      filtered = filtered.filter(
        (user) =>
          user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
          user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
          user.employee_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (departmentFilter !== "all") {
      filtered = filtered.filter(
        (user) => user.department === departmentFilter
      );
    }

    if (roleFilter !== "all") {
      filtered = filtered.filter((user) => user.role === roleFilter);
    }

    if (statusFilter !== "all") {
      if (statusFilter === "active") {
        filtered = filtered.filter(
          (user) => user.is_active && user.is_active_user
        );
      } else if (statusFilter === "inactive") {
        filtered = filtered.filter(
          (user) => !user.is_active || !user.is_active_user
        );
      }
    }

    setFilteredUsers(filtered);
  }, [users, searchTerm, departmentFilter, roleFilter, statusFilter]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/auth/users/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setUsers(data.results || data);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching users:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDepartmentRegistrations = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/devices/departments/registrations/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setRegistrations(data.results || data);
      }
    } catch (error) {
      console.error("Error fetching department registrations:", error);
    }
  };

  const handleCreateUser = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/auth/users/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newUser),
        }
      );

      if (response.ok) {
        fetchUsers();
        setIsCreateUserOpen(false);
        setNewUser({
          username: "",
          email: "",
          full_name: "",
          phone_number: "",
          employee_id: "",
          password: "",
          password_confirm: "",
          department: "",
          role: "",
          district_id: "",
          badge_number: "",
          rank: "",
          years_of_service: 0,
          certifications: "",
        });
      }
    } catch (error) {
      console.error("Error creating user:", error);
    }
  };

  const handleApproveRegistration = async (
    registrationId: string,
    reviewNotes = ""
  ) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `https://my-guardian-plus.onrender.com/api/devices/departments/registrations/${registrationId}/approve/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ review_notes: reviewNotes }),
        }
      );

      if (response.ok) {
        fetchDepartmentRegistrations();
        fetchUsers(); // Refresh users as a new regional manager was created
        setIsRegistrationDetailsOpen(false);
      }
    } catch (error) {
      console.error("Error approving registration:", error);
    }
  };

  const handleRejectRegistration = async (
    registrationId: string,
    reviewNotes: string
  ) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `https://my-guardian-plus.onrender.com/api/devices/departments/registrations/${registrationId}/reject/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ review_notes: reviewNotes }),
        }
      );

      if (response.ok) {
        fetchDepartmentRegistrations();
        setIsRegistrationDetailsOpen(false);
      }
    } catch (error) {
      console.error("Error rejecting registration:", error);
    }
  };

  const toggleUserStatus = async (userId: string, currentStatus: boolean) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `https://my-guardian-plus.onrender.com/api/auth/users/${userId}/`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ is_active_user: !currentStatus }),
        }
      );

      if (response.ok) {
        fetchUsers();
      }
    } catch (error) {
      console.error("Error updating user status:", error);
    }
  };

  if (!user || loading) return <div>Loading...</div>;

  const getDepartmentIcon = (dept: string) => {
    switch (dept) {
      case "fire":
        return <Flame className="h-4 w-4 text-red-500" />;
      case "police":
        return <Shield className="h-4 w-4 text-blue-500" />;
      case "medical":
        return <Heart className="h-4 w-4 text-green-500" />;
      case "admin":
        return <Shield className="h-4 w-4 text-gray-800" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending":
        return "outline";
      case "approved":
        return "default";
      case "rejected":
        return "destructive";
      case "suspended":
        return "secondary";
      default:
        return "secondary";
    }
  };

  const pendingRegistrations = registrations.filter(
    (r) => r.status === "pending"
  );

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">User Management</h1>
              <p className="text-muted-foreground">
                Manage all users and department registration requests
              </p>
            </div>
            <Dialog open={isCreateUserOpen} onOpenChange={setIsCreateUserOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Create User
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>Create New User</DialogTitle>
                  <DialogDescription>
                    Create a new user account for any department
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="username">Username</Label>
                      <Input
                        id="username"
                        value={newUser.username}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            username: e.target.value,
                          }))
                        }
                        placeholder="Enter username"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={newUser.email}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            email: e.target.value,
                          }))
                        }
                        placeholder="Enter email address"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="full_name">Full Name</Label>
                    <Input
                      id="full_name"
                      value={newUser.full_name}
                      onChange={(e) =>
                        setNewUser((prev) => ({
                          ...prev,
                          full_name: e.target.value,
                        }))
                      }
                      placeholder="Enter full name"
                    />
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="phone_number">Phone Number</Label>
                      <Input
                        id="phone_number"
                        value={newUser.phone_number}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            phone_number: e.target.value,
                          }))
                        }
                        placeholder="+265991234567"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="employee_id">Employee ID</Label>
                      <Input
                        id="employee_id"
                        value={newUser.employee_id}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            employee_id: e.target.value,
                          }))
                        }
                        placeholder="EMP001"
                      />
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input
                        id="password"
                        type="password"
                        value={newUser.password}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            password: e.target.value,
                          }))
                        }
                        placeholder="Enter password"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password_confirm">Confirm Password</Label>
                      <Input
                        id="password_confirm"
                        type="password"
                        value={newUser.password_confirm}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            password_confirm: e.target.value,
                          }))
                        }
                        placeholder="Confirm password"
                      />
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="department">Department</Label>
                      <Select
                        value={newUser.department}
                        onValueChange={(value) =>
                          setNewUser((prev) => ({ ...prev, department: value }))
                        }
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select department" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="fire">Fire Department</SelectItem>
                          <SelectItem value="police">
                            Police Department
                          </SelectItem>
                          <SelectItem value="medical">
                            Medical Department
                          </SelectItem>
                          <SelectItem value="admin">
                            System Administrator
                          </SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="role">Role</Label>
                      <Select
                        value={newUser.role}
                        onValueChange={(value) =>
                          setNewUser((prev) => ({ ...prev, role: value }))
                        }
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select role" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="System Administrator">
                            System Administrator
                          </SelectItem>
                          <SelectItem value="Regional Manager">
                            Regional Manager
                          </SelectItem>
                          <SelectItem value="District Manager">
                            District Manager
                          </SelectItem>
                          <SelectItem value="Field User">Field User</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="badge_number">Badge Number</Label>
                      <Input
                        id="badge_number"
                        value={newUser.badge_number}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            badge_number: e.target.value,
                          }))
                        }
                        placeholder="Badge number"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="rank">Rank</Label>
                      <Input
                        id="rank"
                        value={newUser.rank}
                        onChange={(e) =>
                          setNewUser((prev) => ({
                            ...prev,
                            rank: e.target.value,
                          }))
                        }
                        placeholder="Officer rank"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="years_of_service">Years of Service</Label>
                    <Input
                      id="years_of_service"
                      type="number"
                      value={newUser.years_of_service}
                      onChange={(e) =>
                        setNewUser((prev) => ({
                          ...prev,
                          years_of_service: Number.parseInt(e.target.value),
                        }))
                      }
                      placeholder="0"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="certifications">Certifications</Label>
                    <Textarea
                      id="certifications"
                      value={newUser.certifications}
                      onChange={(e) =>
                        setNewUser((prev) => ({
                          ...prev,
                          certifications: e.target.value,
                        }))
                      }
                      placeholder="Professional certifications"
                      rows={3}
                    />
                  </div>

                  <div className="flex gap-2 pt-4">
                    <Button onClick={handleCreateUser} className="flex-1">
                      <Users className="h-4 w-4 mr-2" />
                      Create User
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => setIsCreateUserOpen(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Pending Registrations Alert */}
          {pendingRegistrations.length > 0 && (
            <Card className="border-yellow-200 bg-yellow-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-yellow-700">
                  <AlertTriangle className="h-5 w-5" />
                  Pending Department Registrations (
                  {pendingRegistrations.length})
                </CardTitle>
                <CardDescription className="text-yellow-600">
                  New department registration requests awaiting approval
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {pendingRegistrations.slice(0, 3).map((registration) => (
                    <div
                      key={registration.registration_id}
                      className="flex items-center justify-between p-3 bg-white border border-yellow-200 rounded"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          {getDepartmentIcon(registration.department_type)}
                          <span className="font-medium">
                            {registration.department_name}
                          </span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {registration.contact_person} -{" "}
                          {registration.contact_email}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Submitted:{" "}
                          {new Date(
                            registration.submitted_at
                          ).toLocaleDateString()}
                        </p>
                      </div>
                      <Button
                        size="sm"
                        onClick={() => {
                          setSelectedRegistration(registration);
                          setIsRegistrationDetailsOpen(true);
                        }}
                      >
                        Review
                      </Button>
                    </div>
                  ))}
                  {pendingRegistrations.length > 3 && (
                    <p className="text-sm text-muted-foreground text-center">
                      +{pendingRegistrations.length - 3} more registrations
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Statistics Cards */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Users
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{users.length}</div>
                <p className="text-xs text-muted-foreground">
                  All registered users
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Users
                </CardTitle>
                <UserCheck className="h-4 w-4 text-green-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {users.filter((u) => u.is_active && u.is_active_user).length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Currently active
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Pending Registrations
                </CardTitle>
                <Clock className="h-4 w-4 text-yellow-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {pendingRegistrations.length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Awaiting approval
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Departments
                </CardTitle>
                <Building className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {new Set(users.map((u) => u.department)).size}
                </div>
                <p className="text-xs text-muted-foreground">
                  Active departments
                </p>
              </CardContent>
            </Card>
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList>
              <TabsTrigger value="users">All Users</TabsTrigger>
              <TabsTrigger value="registrations">
                Department Registrations
                {pendingRegistrations.length > 0 && (
                  <Badge variant="destructive" className="ml-2">
                    {pendingRegistrations.length}
                  </Badge>
                )}
              </TabsTrigger>
            </TabsList>

            <TabsContent value="users" className="space-y-4">
              {/* Filters */}
              <Card>
                <CardHeader>
                  <CardTitle>Search & Filter Users</CardTitle>
                  <CardDescription>
                    Find users by name, username, email, or employee ID
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-col gap-4 md:flex-row md:items-center">
                    <div className="flex-1">
                      <div className="relative">
                        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          placeholder="Search users..."
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          className="pl-10"
                        />
                      </div>
                    </div>
                    <Select
                      value={departmentFilter}
                      onValueChange={setDepartmentFilter}
                    >
                      <SelectTrigger className="w-full md:w-[180px]">
                        <SelectValue placeholder="Filter by department" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Departments</SelectItem>
                        <SelectItem value="fire">Fire Department</SelectItem>
                        <SelectItem value="police">
                          Police Department
                        </SelectItem>
                        <SelectItem value="medical">
                          Medical Department
                        </SelectItem>
                        <SelectItem value="admin">System Admin</SelectItem>
                      </SelectContent>
                    </Select>
                    <Select value={roleFilter} onValueChange={setRoleFilter}>
                      <SelectTrigger className="w-full md:w-[180px]">
                        <SelectValue placeholder="Filter by role" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Roles</SelectItem>
                        <SelectItem value="System Administrator">
                          System Administrator
                        </SelectItem>
                        <SelectItem value="Regional Manager">
                          Regional Manager
                        </SelectItem>
                        <SelectItem value="District Manager">
                          District Manager
                        </SelectItem>
                        <SelectItem value="Field User">Field User</SelectItem>
                      </SelectContent>
                    </Select>
                    <Select
                      value={statusFilter}
                      onValueChange={setStatusFilter}
                    >
                      <SelectTrigger className="w-full md:w-[180px]">
                        <SelectValue placeholder="Filter by status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Status</SelectItem>
                        <SelectItem value="active">Active</SelectItem>
                        <SelectItem value="inactive">Inactive</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>

              {/* Users Table */}
              <Card>
                <CardHeader>
                  <CardTitle>Users ({filteredUsers.length})</CardTitle>
                  <CardDescription>
                    Manage all system users across departments
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>User</TableHead>
                          <TableHead>Department</TableHead>
                          <TableHead>Role</TableHead>
                          <TableHead>District</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead>Last Login</TableHead>
                          <TableHead>Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {filteredUsers.map((user) => (
                          <TableRow key={user.id}>
                            <TableCell>
                              <div>
                                <div className="font-medium">
                                  {user.full_name}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  {user.email}
                                </div>
                                <div className="text-xs text-muted-foreground">
                                  {user.employee_id} • {user.badge_number}
                                </div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                {getDepartmentIcon(user.department)}
                                <span>{user.department_display}</span>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">{user.role}</Badge>
                            </TableCell>
                            <TableCell>
                              <div className="text-sm">
                                {user.district_name || "N/A"}
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                {user.is_active && user.is_active_user ? (
                                  <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : (
                                  <XCircle className="h-4 w-4 text-red-500" />
                                )}
                                <Badge
                                  variant={
                                    user.is_active && user.is_active_user
                                      ? "default"
                                      : "secondary"
                                  }
                                >
                                  {user.is_active && user.is_active_user
                                    ? "Active"
                                    : "Inactive"}
                                </Badge>
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="text-sm">
                                {user.last_login
                                  ? new Date(
                                      user.last_login
                                    ).toLocaleDateString()
                                  : "Never"}
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() =>
                                    toggleUserStatus(
                                      user.id,
                                      user.is_active_user
                                    )
                                  }
                                >
                                  {user.is_active_user ? (
                                    <UserX className="h-4 w-4" />
                                  ) : (
                                    <UserCheck className="h-4 w-4" />
                                  )}
                                </Button>
                                <Button variant="ghost" size="sm">
                                  <Edit className="h-4 w-4" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="text-red-600 hover:text-red-700"
                                >
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
            </TabsContent>

            <TabsContent value="registrations" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Department Registration Requests</CardTitle>
                  <CardDescription>
                    Review and approve new department registrations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Department</TableHead>
                          <TableHead>Contact Person</TableHead>
                          <TableHead>Location</TableHead>
                          <TableHead>Population Served</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead>Submitted</TableHead>
                          <TableHead>Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {registrations.map((registration) => (
                          <TableRow key={registration.registration_id}>
                            <TableCell>
                              <div>
                                <div className="flex items-center gap-2">
                                  {getDepartmentIcon(
                                    registration.department_type
                                  )}
                                  <span className="font-medium">
                                    {registration.department_name}
                                  </span>
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  {registration.registration_number}
                                </div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <div>
                                <div className="font-medium">
                                  {registration.contact_person}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  {registration.contact_email}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                  {registration.contact_phone}
                                </div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="text-sm">
                                {registration.city}, {registration.state}
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="text-sm">
                                {registration.population_served.toLocaleString()}
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge
                                variant={
                                  getStatusColor(registration.status) as any
                                }
                              >
                                {registration.status}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <div className="text-sm">
                                {new Date(
                                  registration.submitted_at
                                ).toLocaleDateString()}
                              </div>
                            </TableCell>
                            <TableCell>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => {
                                  setSelectedRegistration(registration);
                                  setIsRegistrationDetailsOpen(true);
                                }}
                              >
                                Review
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Registration Details Dialog */}
          <Dialog
            open={isRegistrationDetailsOpen}
            onOpenChange={setIsRegistrationDetailsOpen}
          >
            <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Department Registration Review</DialogTitle>
                <DialogDescription>
                  Review and approve/reject department registration request
                </DialogDescription>
              </DialogHeader>
              {selectedRegistration && (
                <div className="space-y-6">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label className="text-sm font-medium">
                        Department Name
                      </Label>
                      <p className="text-sm">
                        {selectedRegistration.department_name}
                      </p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">
                        Department Type
                      </Label>
                      <div className="flex items-center gap-2">
                        {getDepartmentIcon(
                          selectedRegistration.department_type
                        )}
                        <span className="text-sm">
                          {selectedRegistration.department_type}
                        </span>
                      </div>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">
                        Registration Number
                      </Label>
                      <p className="text-sm">
                        {selectedRegistration.registration_number}
                      </p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">
                        Population Served
                      </Label>
                      <p className="text-sm">
                        {selectedRegistration.population_served.toLocaleString()}
                      </p>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Contact Information
                    </Label>
                    <div className="mt-2 space-y-1">
                      <p className="text-sm">
                        <strong>Name:</strong>{" "}
                        {selectedRegistration.contact_person}
                      </p>
                      <p className="text-sm">
                        <strong>Email:</strong>{" "}
                        {selectedRegistration.contact_email}
                      </p>
                      <p className="text-sm">
                        <strong>Phone:</strong>{" "}
                        {selectedRegistration.contact_phone}
                      </p>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">Address</Label>
                    <p className="text-sm mt-1">
                      {selectedRegistration.address},{" "}
                      {selectedRegistration.city}, {selectedRegistration.state}{" "}
                      {selectedRegistration.zip_code},{" "}
                      {selectedRegistration.country}
                    </p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Coverage Description
                    </Label>
                    <p className="text-sm mt-1">
                      {selectedRegistration.coverage_description}
                    </p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Regional Manager Information
                    </Label>
                    <div className="mt-2 space-y-1">
                      <p className="text-sm">
                        <strong>Name:</strong>{" "}
                        {selectedRegistration.regional_manager_name}
                      </p>
                      <p className="text-sm">
                        <strong>Email:</strong>{" "}
                        {selectedRegistration.regional_manager_email}
                      </p>
                      <p className="text-sm">
                        <strong>Phone:</strong>{" "}
                        {selectedRegistration.regional_manager_phone}
                      </p>
                      <p className="text-sm">
                        <strong>Credentials:</strong>{" "}
                        {selectedRegistration.regional_manager_credentials}
                      </p>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Submission Date
                    </Label>
                    <p className="text-sm">
                      {new Date(
                        selectedRegistration.submitted_at
                      ).toLocaleString()}
                    </p>
                  </div>

                  {selectedRegistration.status === "pending" && (
                    <div className="flex gap-2 pt-4">
                      <Button
                        onClick={() =>
                          handleApproveRegistration(
                            selectedRegistration.registration_id
                          )
                        }
                        className="flex-1"
                      >
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Approve Registration
                      </Button>
                      <Button
                        variant="destructive"
                        onClick={() =>
                          handleRejectRegistration(
                            selectedRegistration.registration_id,
                            "Rejected by administrator"
                          )
                        }
                        className="flex-1"
                      >
                        <XCircle className="h-4 w-4 mr-2" />
                        Reject Registration
                      </Button>
                    </div>
                  )}

                  {selectedRegistration.status !== "pending" && (
                    <div className="p-4 bg-gray-50 rounded">
                      <Label className="text-sm font-medium">
                        Review Status
                      </Label>
                      <p className="text-sm mt-1">
                        <Badge
                          variant={
                            getStatusColor(selectedRegistration.status) as any
                          }
                        >
                          {selectedRegistration.status}
                        </Badge>
                      </p>
                      {selectedRegistration.review_notes && (
                        <p className="text-sm mt-2">
                          <strong>Notes:</strong>{" "}
                          {selectedRegistration.review_notes}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              )}
            </DialogContent>
          </Dialog>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
