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
  AlertTriangle,
  UserPlus,
  Shield,
  Flame,
  Heart,
  Clock,
  MapPin,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function StationManagerDashboard() {
  const [user, setUser] = useState(null);
  const [staff, setStaff] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({
    total_responders: 0,
    active_alerts: 0,
    on_duty: 0,
  });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
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
      
      // Fetch staff hierarchy
      const hierarchyResponse = await fetch(
        `${process.env.BACKEND_URL}/auth/admin/hierarchy/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      
      if (hierarchyResponse.ok) {
        const hierarchyData = await hierarchyResponse.json();
        const allStaff = [
          ...(hierarchyData.responders || []),
          ...(hierarchyData.field_users || [])
        ];
        setStaff(allStaff);
        setStats(prev => ({ 
          ...prev, 
          total_responders: allStaff.length,
          on_duty: allStaff.filter(s => s.is_active).length
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
      case "fire": return <Flame className="h-4 w-4 text-red-500" />;
      case "police": return <Shield className="h-4 w-4 text-blue-500" />;
      case "medical": return <Heart className="h-4 w-4 text-green-500" />;
      default: return <Users className="h-4 w-4 text-gray-500" />;
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
              <h1 className="text-3xl font-bold text-gray-900">Station Management</h1>
              <p className="text-muted-foreground">
                {user.department} Department • {user.station_name}
              </p>
            </div>
            <Button asChild>
              <Link href="/dashboard/station/create-responder">
                <UserPlus className="h-4 w-4 mr-2" />
                Add Responder
              </Link>
            </Button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Responders</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_responders}</div>
                <p className="text-xs text-muted-foreground">
                  Responders in your station
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">On Duty</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.on_duty}</div>
                <p className="text-xs text-muted-foreground">
                  Currently active responders
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.active_alerts}</div>
                <p className="text-xs text-muted-foreground">
                  Current emergency alerts
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <Tabs defaultValue="responders" className="space-y-4">
            <TabsList>
              <TabsTrigger value="responders">Responders</TabsTrigger>
              <TabsTrigger value="alerts">Station Alerts</TabsTrigger>
              <TabsTrigger value="schedule">Schedule</TabsTrigger>
            </TabsList>

            <TabsContent value="responders" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Station Responders</CardTitle>
                  <CardDescription>
                    Manage responders and field users in your station
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : staff.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No responders found. Add your first responder to get started.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {staff.map((member) => (
                        <div
                          key={member.id}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                              {getDepartmentIcon(member.department)}
                              <div>
                                <h4 className="font-medium">{member.full_name}</h4>
                                <p className="text-sm text-muted-foreground">
                                  {member.role} • {member.email}
                                </p>
                                {member.badge_number && (
                                  <p className="text-xs text-muted-foreground">
                                    Badge: {member.badge_number}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge variant={member.is_active ? "default" : "secondary"}>
                              {member.is_active ? "On Duty" : "Off Duty"}
                            </Badge>
                            <Badge variant="outline">
                              {member.role}
                            </Badge>
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
                  <CardTitle>Station Alerts</CardTitle>
                  <CardDescription>
                    Emergency alerts for your station
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    Station alert management will be implemented here
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="schedule" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Duty Schedule</CardTitle>
                  <CardDescription>
                    Manage responder schedules and shifts
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    Schedule management will be implemented here
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center">
                  <UserPlus className="h-6 w-6 mb-2" />
                  Add New Responder
                </Button>
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center">
                  <AlertTriangle className="h-6 w-6 mb-2" />
                  Create Alert
                </Button>
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center">
                  <Clock className="h-6 w-6 mb-2" />
                  Update Schedule
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
