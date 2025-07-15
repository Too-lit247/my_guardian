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
  AlertTriangle,
  MapPin,
  Clock,
  CheckCircle,
  Calendar,
  Building,
  Users,
  Phone,
} from "lucide-react";
import AuthWrapper from "@/components/auth-wrapper";

export default function FieldOfficerDashboard() {
  const [user, setUser] = useState(null);
  const [station, setStation] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [myAlerts, setMyAlerts] = useState([]);
  const [stats, setStats] = useState({
    active_alerts: 0,
    my_responses: 0,
    completed_today: 0,
    pending_responses: 0,
  });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);

      // Ensure only field officers can access this page
      if (parsedUser.role !== "Field Officer") {
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
        }
      }

      // Fetch alerts
      const alertsResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/alerts/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (alertsResponse.ok) {
        const alertsData = await alertsResponse.json();
        const allAlerts = alertsData.results || [];
        const activeAlerts = allAlerts.filter(
          (alert) => alert.status === "active"
        );
        const userAlerts = allAlerts.filter(
          (alert) => alert.assigned_to === user?.id
        );
        const todayAlerts = userAlerts.filter((alert) => {
          const alertDate = new Date(alert.created_at).toDateString();
          const today = new Date().toDateString();
          return alertDate === today && alert.status === "resolved";
        });

        setAlerts(allAlerts.slice(0, 10)); // Recent 10 alerts
        setMyAlerts(userAlerts);
        setStats({
          active_alerts: activeAlerts.length,
          my_responses: userAlerts.length,
          completed_today: todayAlerts.length,
          pending_responses: userAlerts.filter((a) => a.status === "active")
            .length,
        });
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

  const getStatusColor = (status) => {
    switch (status) {
      case "active":
        return "destructive";
      case "resolved":
        return "default";
      case "investigating":
        return "secondary";
      default:
        return "outline";
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
                Field Officer Dashboard
              </h1>
              <p className="text-muted-foreground">
                Monitor and respond to emergency alerts
              </p>
              {station && (
                <p className="text-sm text-muted-foreground mt-1">
                  <Building className="h-4 w-4 inline mr-1" />
                  {station.name} ({station.code})
                </p>
              )}
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Alerts
                </CardTitle>
                <AlertTriangle className="h-4 w-4 text-red-500" />
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
                  My Responses
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.my_responses}</div>
                <p className="text-xs text-muted-foreground">
                  Total alerts assigned to me
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Completed Today
                </CardTitle>
                <CheckCircle className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.completed_today}
                </div>
                <p className="text-xs text-muted-foreground">
                  Alerts resolved today
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Pending</CardTitle>
                <Clock className="h-4 w-4 text-yellow-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.pending_responses}
                </div>
                <p className="text-xs text-muted-foreground">
                  Awaiting my response
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Station Information */}
          {station && (
            <Card>
              <CardHeader>
                <CardTitle>My Station</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <Building className="h-4 w-4 text-muted-foreground" />
                        <span className="font-medium">{station.name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4 text-muted-foreground" />
                        <span>
                          {station.address}, {station.city}
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
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="font-medium">Department:</span>{" "}
                        {station.district?.department}
                      </div>
                      <div>
                        <span className="font-medium">Region:</span>{" "}
                        {station.district?.region}
                      </div>
                      <div>
                        <span className="font-medium">Type:</span>{" "}
                        {station.station_type}
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Tabs defaultValue="all-alerts" className="space-y-4">
            <TabsList>
              <TabsTrigger value="all-alerts">All Alerts</TabsTrigger>
              <TabsTrigger value="my-alerts">My Alerts</TabsTrigger>
            </TabsList>

            <TabsContent value="all-alerts" className="space-y-4">
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
                  ) : alerts.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No alerts found
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {alerts.map((alert) => (
                        <div
                          key={alert.alert_id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                        >
                          <div className="flex items-center space-x-4">
                            <div>
                              <h4 className="font-medium">
                                {alert.alert_type}
                              </h4>
                              <p className="text-sm text-muted-foreground">
                                {alert.description}
                              </p>
                              <div className="flex items-center gap-4 mt-1">
                                <p className="text-xs text-muted-foreground">
                                  <Calendar className="h-3 w-3 inline mr-1" />
                                  {new Date(alert.created_at).toLocaleString()}
                                </p>
                                {alert.location && (
                                  <p className="text-xs text-muted-foreground">
                                    <MapPin className="h-3 w-3 inline mr-1" />
                                    {alert.location}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              className={getAlertSeverityColor(alert.severity)}
                            >
                              {alert.severity}
                            </Badge>
                            <Badge variant={getStatusColor(alert.status)}>
                              {alert.status}
                            </Badge>
                            <Button variant="outline" size="sm">
                              Respond
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="my-alerts" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>My Assigned Alerts</CardTitle>
                  <CardDescription>
                    Alerts assigned to you for response
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : myAlerts.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No alerts assigned to you
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {myAlerts.map((alert) => (
                        <div
                          key={alert.alert_id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                        >
                          <div className="flex items-center space-x-4">
                            <div>
                              <h4 className="font-medium">
                                {alert.alert_type}
                              </h4>
                              <p className="text-sm text-muted-foreground">
                                {alert.description}
                              </p>
                              <div className="flex items-center gap-4 mt-1">
                                <p className="text-xs text-muted-foreground">
                                  <Calendar className="h-3 w-3 inline mr-1" />
                                  {new Date(alert.created_at).toLocaleString()}
                                </p>
                                {alert.location && (
                                  <p className="text-xs text-muted-foreground">
                                    <MapPin className="h-3 w-3 inline mr-1" />
                                    {alert.location}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge
                              className={getAlertSeverityColor(alert.severity)}
                            >
                              {alert.severity}
                            </Badge>
                            <Badge variant={getStatusColor(alert.status)}>
                              {alert.status}
                            </Badge>
                            <Button variant="outline" size="sm">
                              Update
                            </Button>
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
