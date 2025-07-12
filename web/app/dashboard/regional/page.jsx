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

export default function RegionalManagerDashboard() {
  const [user, setUser] = useState(null);
  const [districts, setDistricts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [staff, setStaff] = useState([]);
  const [stats, setStats] = useState({
    total_districts: 0,
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
      
      if (parsedUser.role !== "Regional Manager") {
        router.push("/dashboard");
        return;
      }
      
      fetchData();
    }
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("access_token");
      
      // Fetch districts
      const districtsResponse = await fetch(
        `${process.env.BACKEND_URL}/geography/districts/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      
      if (districtsResponse.ok) {
        const districtsData = await districtsResponse.json();
        setDistricts(districtsData);
        setStats(prev => ({ ...prev, total_districts: districtsData.length }));
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
          ...(hierarchyData.district_managers || []),
          ...(hierarchyData.station_managers || []),
          ...(hierarchyData.responders || []),
          ...(hierarchyData.field_users || [])
        ];
        setStaff(allStaff);
        setStats(prev => ({ ...prev, total_staff: allStaff.length }));
      }

      // Fetch alerts (you'll need to implement this endpoint)
      // const alertsResponse = await fetch(...);

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
              <h1 className="text-3xl font-bold text-gray-900">Regional Management</h1>
              <p className="text-muted-foreground">
                {user.department} Department • {user.region_display}
              </p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" asChild>
                <Link href="/dashboard/regional/create-district">
                  <Plus className="h-4 w-4 mr-2" />
                  Add District
                </Link>
              </Button>
              <Button asChild>
                <Link href="/dashboard/regional/create-user">
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
                <CardTitle className="text-sm font-medium">Districts</CardTitle>
                <Building className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_districts}</div>
                <p className="text-xs text-muted-foreground">
                  Districts in your region
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
          <Tabs defaultValue="districts" className="space-y-4">
            <TabsList>
              <TabsTrigger value="districts">Districts</TabsTrigger>
              <TabsTrigger value="staff">Staff</TabsTrigger>
              <TabsTrigger value="alerts">Alerts</TabsTrigger>
            </TabsList>

            <TabsContent value="districts" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Districts in Your Region</CardTitle>
                  <CardDescription>
                    Manage districts and assign district managers
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="text-center py-8">Loading...</div>
                  ) : districts.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No districts found. Create your first district to get started.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {districts.map((district) => (
                        <div
                          key={district.district_id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                        >
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                              {getDepartmentIcon(district.department)}
                              <div>
                                <h4 className="font-medium">{district.name}</h4>
                                <p className="text-sm text-muted-foreground">
                                  {district.city} • {district.station_count} stations • {district.staff_count} staff
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            <Badge variant={district.manager_name ? "default" : "outline"}>
                              {district.manager_name || "No Manager"}
                            </Badge>
                            <Button variant="outline" size="sm" asChild>
                              <Link href={`/dashboard/regional/districts/${district.district_id}`}>
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
                  <CardTitle>Regional Staff</CardTitle>
                  <CardDescription>
                    All staff members in your region
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
                                {member.role} • {member.email}
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
                  <CardTitle>Regional Alerts</CardTitle>
                  <CardDescription>
                    Emergency alerts in your region
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
