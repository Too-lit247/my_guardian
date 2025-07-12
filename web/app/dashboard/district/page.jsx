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
  Building,
  Users,
  AlertTriangle,
  Plus,
  MapPin,
  Shield,
  Flame,
  Heart,
  Eye,
  UserPlus,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function DistrictManagerDashboard() {
  const [user, setUser] = useState(null);
  const [stations, setStations] = useState([]);
  const [staff, setStaff] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({
    total_stations: 0,
    total_staff: 0,
    active_alerts: 0,
  });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      if (parsedUser.role !== "District Manager") {
        router.push("/dashboard");
        return;
      }
      
      fetchData();
    }
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("access_token");
      
      // Fetch stations in this district
      const stationsResponse = await fetch(
        `${process.env.BACKEND_URL}/geography/stations/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      
      if (stationsResponse.ok) {
        const stationsData = await stationsResponse.json();
        setStations(stationsData);
        setStats(prev => ({ ...prev, total_stations: stationsData.length }));
      }

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
          ...(hierarchyData.station_managers || []),
          ...(hierarchyData.responders || []),
          ...(hierarchyData.field_users || [])
        ];
        setStaff(allStaff);
        setStats(prev => ({ ...prev, total_staff: allStaff.length }));
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
      default: return <Building className="h-4 w-4 text-gray-500" />;
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
              <h1 className="text-3xl font-bold text-gray-900">District Management</h1>
              <p className="text-muted-foreground">
                {user.department} Department • {user.district_name}
              </p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" asChild>
                <Link href="/dashboard/district/create-station">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Station
                </Link>
              </Button>
              <Button asChild>
                <Link href="/dashboard/district/create-user">
                  <UserPlus className="h-4 w-4 mr-2" />
                  Create User
                </Link>
              </Button>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Stations</CardTitle>
                <Building className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_stations}</div>
                <p className="text-xs text-muted-foreground">
                  Stations in your district
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Staff Members</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_staff}</div>
                <p className="text-xs text-muted-foreground">
                  Total staff under management
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
          <Tabs defaultValue="stations" className="space-y-4">
            <TabsList>
              <TabsTrigger value="stations">Stations</TabsTrigger>
              <TabsTrigger value="staff">Staff</TabsTrigger>
              <TabsTrigger value="alerts">Alerts</TabsTrigger>
            </TabsList>

            <TabsContent value="stations" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Stations in Your District</CardTitle>
                  <CardDescription>
                    Manage stations and assign station managers
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : stations.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No stations found. Create your first station to get started.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {stations.map((station) => (
                        <div
                          key={station.station_id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                              <Building className="h-5 w-5 text-blue-500" />
                              <div>
                                <h4 className="font-medium">{station.name}</h4>
                                <p className="text-sm text-muted-foreground">
                                  {station.station_type} • {station.staff_count} staff
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            <Badge variant={station.manager_name ? "default" : "outline"}>
                              {station.manager_name || "No Manager"}
                            </Badge>
                            <Button variant="outline" size="sm" asChild>
                              <Link href={`/dashboard/district/stations/${station.station_id}`}>
                                <Eye className="h-4 w-4 mr-1" />
                                Manage
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

            <TabsContent value="staff" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>District Staff</CardTitle>
                  <CardDescription>
                    All staff members in your district
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : staff.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No staff members found
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {staff.map((member) => (
                        <div
                          key={member.id}
                          className="flex items-center justify-between p-4 border rounded-lg"
                        >
                          <div className="flex items-center space-x-4">
                            <div>
                              <h4 className="font-medium">{member.full_name}</h4>
                              <p className="text-sm text-muted-foreground">
                                {member.role} • {member.station_name || "No Station"} • {member.email}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge variant={member.is_active ? "default" : "secondary"}>
                              {member.is_active ? "Active" : "Inactive"}
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
                  <CardTitle>District Alerts</CardTitle>
                  <CardDescription>
                    Emergency alerts in your district
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    Alert management will be implemented here
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
