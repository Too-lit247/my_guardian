"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Search, Plus, Edit, Trash2 } from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";

interface User {
  email: string;
  department: string;
  role: string;
  name: string;
  id: string;
}

interface SystemUser {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  district: string;
  status: "Active" | "Inactive";
  createdAt: string;
}

export default function UsersPage() {
  const [user, setUser] = useState<User | null>(null);
  const [users, setUsers] = useState<SystemUser[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<SystemUser[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      router.push("/");
      return;
    }
    const currentUser = JSON.parse(userData);
    setUser(currentUser);

    fetchUsers();
  }, [router]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/users/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.ok) {
        const data = await response.json();
        const backendUsers =
          data.results?.map((u: any) => ({
            id: u.id,
            name: u.full_name,
            email: u.email,
            role: u.role,
            department: u.department,
            district: u.station_id || "Unassigned",
            status: u.is_active ? "Active" : "Inactive",
            createdAt: u.date_joined || new Date().toISOString(),
          })) || [];

        setUsers(backendUsers);
        setFilteredUsers(backendUsers);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  useEffect(() => {
    const filtered = users.filter(
      (user) =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.district.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredUsers(filtered);
  }, [users, searchTerm]);

  if (!user) return null;

  const canAddUsers = ["Admin", "Station Manager"].includes(user.role);

  return (
    <AuthWrapper allowedRoles={["Admin", "Station Manager"]}>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">User Management</h1>
              <p className="text-muted-foreground">
                Manage users in the system
              </p>
            </div>
            {canAddUsers && (
              <Button asChild>
                <Link href="/dashboard/field-officers/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Add New User
                </Link>
              </Button>
            )}
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Search Users</CardTitle>
              <CardDescription>
                Find users by name, email, or district
              </CardDescription>
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
                        <TableCell className="font-medium">
                          {systemUser.name}
                        </TableCell>
                        <TableCell>{systemUser.email}</TableCell>
                        <TableCell>
                          <Badge variant="outline" className="capitalize">
                            {systemUser.role}
                          </Badge>
                        </TableCell>
                        <TableCell>{systemUser.district}</TableCell>
                        <TableCell>
                          <Badge
                            variant={
                              systemUser.status === "Active"
                                ? "default"
                                : "secondary"
                            }
                          >
                            {systemUser.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {new Date(systemUser.createdAt).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
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
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
