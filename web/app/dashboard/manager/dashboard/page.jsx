"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/dashboard-layout";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Building,
  Users,
  AlertTriangle,
  Plus,
  Eye,
  MapPin,
  Phone,
  Mail,
  Calendar,
} from "lucide-react";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function ManagerDashboard() {
  const [user, setUser] = useState(null);
  const [station, setStation] = useState(null);
  const [fieldOfficers, setFieldOfficers] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [stats, setStats] = useState({
    total_field_officers: 0,
    active_alerts: 0,
    station_capacity: 0,
    current_staff: 0,
  });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);

      // Ensure only station managers can access this page
      if (parsedUser.role !== "Station Manager") {
        router.push("/dashboard");
        return;
      }

      fetchData();
    }
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("access_token");

      // Fetch station information
      if (user?.station_id) {
        const stationResponse = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/geography/stations/${user.station_id}/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (stationResponse.ok) {
          const stationData = await stationResponse.json();
          setStation(stationData);
          setStats((prev) => ({
            ...prev,
            station_capacity: stationData.capacity || 0,
            current_staff: stationData.staff_count || 0,
          }));
        }
      }

      // Fetch field officers under this station
      const usersResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/users/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (usersResponse.ok) {
        const usersData = await usersResponse.json();
        const stationFieldOfficers =
          usersData.results?.filter(
            (u) =>
              u.role === "Field Officer" && u.station_id === user?.station_id
          ) || [];
        setFieldOfficers(stationFieldOfficers);
        setStats((prev) => ({
          ...prev,
          total_field_officers: stationFieldOfficers.length,
        }));
      }

      // Fetch recent alerts
      const alertsResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/alerts/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (alertsResponse.ok) {
        const alertsData = await alertsResponse.json();
        const activeAlerts =
          alertsData.results?.filter((alert) => alert.status === "active") ||
          [];
        setRecentAlerts(alertsData.results?.slice(0, 5) || []);
        setStats((prev) => ({
          ...prev,
          active_alerts: activeAlerts.length,
        }));
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getAlertSeverityColor = (severity) => {
    switch (severity) {
      case "critical":
        return "bg-red-100 text-red-800";
      case "high":
        return "bg-orange-100 text-orange-800";
      case "medium":
        return "bg-yellow-100 text-yellow-800";
      case "low":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Station Manager Dashboard
              </h1>
              <p className="text-muted-foreground">
                Manage your station and field officers
              </p>
              {station && (
                <p className="text-sm text-muted-foreground mt-1">
                  <Building className="h-4 w-4 inline mr-1" />
                  {station.name} ({station.code})
                </p>
              )}
            </div>
            <Button asChild>
              <Link href="/dashboard/manager/add-officer">
                <Plus className="h-4 w-4 mr-2" />
                Add Field Officer
              </Link>
            </Button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Field Officers
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.total_field_officers}
                </div>
                <p className="text-xs text-muted-foreground">
                  Officers under your command
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Alerts
                </CardTitle>
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.active_alerts}</div>
                <p className="text-xs text-muted-foreground">
                  Alerts requiring attention
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Station Capacity
                </CardTitle>
                <Building className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.current_staff}/{stats.station_capacity}
                </div>
                <p className="text-xs text-muted-foreground">
                  Current staffing level
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Station Status
                </CardTitle>
                <Building className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {station?.is_active ? "Active" : "Inactive"}
                </div>
                <p className="text-xs text-muted-foreground">
                  Operational status
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Station Information */}
          {station && (
            <Card>
              <CardHeader>
                <CardTitle>Station Information</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium mb-2">Basic Information</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <Building className="h-4 w-4 text-muted-foreground" />
                        <span>
                          {station.name} ({station.code})
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4 text-muted-foreground" />
                        <span>
                          {station.address}, {station.city}, {station.state}
                        </span>
                      </div>
                      {station.phone && (
                        <div className="flex items-center gap-2">
                          <Phone className="h-4 w-4 text-muted-foreground" />
                          <span>{station.phone}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Operational Details</h4>
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="font-medium">Type:</span>{" "}
                        {station.station_type}
                      </div>
                      <div>
                        <span className="font-medium">Department:</span>{" "}
                        {station.district?.department}
                      </div>
                      <div>
                        <span className="font-medium">Region:</span>{" "}
                        {station.district?.region}
                      </div>
                      {station.operating_hours && (
                        <div>
                          <span className="font-medium">Hours:</span>{" "}
                          {station.operating_hours}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Tabs defaultValue="officers" className="space-y-4">
            <TabsList>
              <TabsTrigger value="officers">Field Officers</TabsTrigger>
              <TabsTrigger value="alerts">Recent Alerts</TabsTrigger>
            </TabsList>

            <TabsContent value="officers" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Field Officers</CardTitle>
                  <CardDescription>
                    Manage field officers assigned to your station
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : fieldOfficers.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No field officers assigned to your station
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {fieldOfficers.map((officer) => (
                        <div
                          key={officer.id}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center space-x-4">
                            <div>
                              <h4 className="font-medium">
                                {officer.full_name}
                              </h4>
                              <p className="text-sm text-muted-foreground">
                                <Mail className="h-3 w-3 inline mr-1" />
                                {officer.email}
                              </p>
                              {officer.phone_number && (
                                <p className="text-sm text-muted-foreground">
                                  <Phone className="h-3 w-3 inline mr-1" />
                                  {officer.phone_number}
                                </p>
                              )}
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              variant={
                                officer.is_active ? "default" : "secondary"
                              }
                            >
                              {officer.is_active ? "Active" : "Inactive"}
                            </Badge>
                            <Button variant="outline" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="alerts" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Alerts</CardTitle>
                  <CardDescription>
                    Latest emergency alerts in your area
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : recentAlerts.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No recent alerts
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {recentAlerts.map((alert) => (
                        <div
                          key={alert.alert_id}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center space-x-4">
                            <div>
                              <h4 className="font-medium">
                                {alert.alert_type}
                              </h4>
                              <p className="text-sm text-muted-foreground">
                                {alert.description}
                              </p>
                              <p className="text-xs text-muted-foreground">
                                <Calendar className="h-3 w-3 inline mr-1" />
                                {new Date(alert.created_at).toLocaleString()}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              className={getAlertSeverityColor(alert.severity)}
                            >
                              {alert.severity}
                            </Badge>
                            <Badge
                              variant={
                                alert.status === "active"
                                  ? "destructive"
                                  : "secondary"
                              }
                            >
                              {alert.status}
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
