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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Users,
  Building,
  FileText,
  CheckCircle,
  XCircle,
  Clock,
  Plus,
  Shield,
  Flame,
  Heart,
  Eye,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function AdminDashboard() {
  const [user, setUser] = useState(null);
  const [registrationRequests, setRegistrationRequests] = useState([]);
  const [stationManagers, setStationManagers] = useState([]);
  const [stats, setStats] = useState({
    pending_requests: 0,
    total_station_managers: 0,
    total_users: 0,
    total_stations: 0,
  });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);

      // Allow all users to access admin dashboard (less strict)
      // Frontend will show appropriate content based on user role
      fetchData();
    }
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("access_token");

      // Fetch registration requests
      const requestsResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/registration-requests/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (requestsResponse.ok) {
        const requestsData = await requestsResponse.json();
        setRegistrationRequests(requestsData.results || []);
        setStats((prev) => ({
          ...prev,
          pending_requests:
            requestsData.results?.filter((r) => r.status === "pending")
              .length || 0,
        }));
      }

      // Fetch station managers
      const managersResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/users/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (managersResponse.ok) {
        const managersData = await managersResponse.json();
        const stationManagersData =
          managersData.results?.filter(
            (user) => user.role === "Station Manager"
          ) || [];
        setStationManagers(stationManagersData);
        setStats((prev) => ({
          ...prev,
          total_station_managers: stationManagersData.length,
          total_users: managersData.results?.length || 0,
        }));
      }

      // Fetch stations count
      const stationsResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/geography/stations/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (stationsResponse.ok) {
        const stationsData = await stationsResponse.json();
        setStats((prev) => ({
          ...prev,
          total_stations: stationsData.length || 0,
        }));
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getDepartmentIcon = (dept) => {
    switch (dept) {
      case "fire":
        return <Flame className="h-4 w-4 text-red-500" />;
      case "police":
        return <Shield className="h-4 w-4 text-blue-500" />;
      case "medical":
        return <Heart className="h-4 w-4 text-green-500" />;
      default:
        return <Users className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case "pending":
        return (
          <Badge
            variant="outline"
            className="text-yellow-600 border-yellow-300"
          >
            <Clock className="h-3 w-3 mr-1" />
            Pending
          </Badge>
        );
      case "approved":
        return (
          <Badge variant="outline" className="text-green-600 border-green-300">
            <CheckCircle className="h-3 w-3 mr-1" />
            Approved
          </Badge>
        );
      case "denied":
        return (
          <Badge variant="outline" className="text-red-600 border-red-300">
            <XCircle className="h-3 w-3 mr-1" />
            Denied
          </Badge>
        );
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <AuthWrapper allowedRoles={["Admin", "System Administrator"]}>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                System Administration
              </h1>
              <p className="text-muted-foreground">
                Manage the MyGuardian+ emergency response network
              </p>
            </div>
            <Button asChild>
              <Link href="/dashboard/admin/create-user">
                <Plus className="h-4 w-4 mr-2" />
                Create Admin User
              </Link>
            </Button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Pending Requests
                </CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.pending_requests}
                </div>
                <p className="text-xs text-muted-foreground">
                  Station registration requests awaiting review
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Stations
                </CardTitle>
                <Building className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_stations}</div>
                <p className="text-xs text-muted-foreground">
                  Active emergency response stations
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Station Managers
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.total_station_managers}
                </div>
                <p className="text-xs text-muted-foreground">
                  Active station managers
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Users
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_users}</div>
                <p className="text-xs text-muted-foreground">
                  All registered users
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <Tabs defaultValue="requests" className="space-y-4">
            <TabsList>
              <TabsTrigger value="requests">Registration Requests</TabsTrigger>
              <TabsTrigger value="managers">Station Managers</TabsTrigger>
            </TabsList>

            <TabsContent value="requests" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Station Registration Requests</CardTitle>
                  <CardDescription>
                    Review and approve station registration requests
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : registrationRequests.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No registration requests found
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {registrationRequests.map((request) => (
                        <div
                          key={request.request_id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                              {getDepartmentIcon(request.department)}
                              <div>
                                <h4 className="font-medium">
                                  {request.station_name || request.full_name}
                                </h4>
                                <p className="text-sm text-muted-foreground">
                                  Manager: {request.full_name} •{" "}
                                  {request.department} • {request.region}
                                </p>
                                {request.station_address && (
                                  <p className="text-xs text-muted-foreground">
                                    {request.station_address}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            {getStatusBadge(request.status)}
                            <Button variant="outline" size="sm" asChild>
                              <Link
                                href={`/dashboard/admin/requests/${request.request_id}`}
                              >
                                <Eye className="h-4 w-4 mr-1" />
                                Review
                              </Link>
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="managers" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Station Managers</CardTitle>
                  <CardDescription>
                    Manage station managers across all departments
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : stationManagers.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No station managers found
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {stationManagers.map((manager) => (
                        <div
                          key={manager.id}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                              {getDepartmentIcon(manager.department)}
                              <div>
                                <h4 className="font-medium">
                                  {manager.full_name}
                                </h4>
                                <p className="text-sm text-muted-foreground">
                                  {manager.department} • {manager.region} •{" "}
                                  {manager.email}
                                </p>
                                {manager.station_id && (
                                  <p className="text-xs text-muted-foreground">
                                    Station ID: {manager.station_id}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              variant={
                                manager.is_active ? "default" : "secondary"
                              }
                            >
                              {manager.is_active ? "Active" : "Inactive"}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
