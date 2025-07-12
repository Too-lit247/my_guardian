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
import {
  AlertTriangle,
  Users,
  Building,
  Activity,
  Plus,
  Bell,
  History,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);

      // Redirect based on user role
      switch (parsedUser.role) {
        case "System Administrator":
          router.push("/dashboard/admin");
          return;
        case "Regional Manager":
          router.push("/dashboard/regional");
          return;
        case "District Manager":
          router.push("/dashboard/district");
          return;
        case "Station Manager":
          router.push("/dashboard/station");
          return;
        default:
          // For Responders and Field Users, stay on main dashboard
          fetchStats();
          break;
      }
    }
  }, []);

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/alerts/statistics/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!user || loading) return <div>Loading...</div>;

  const dashboardStats = [
    {
      title: "Active Alerts",
      value: stats?.active_alerts || "0",
      description: "Current emergency situations",
      icon: AlertTriangle,
      color: "text-red-500",
    },
    {
      title: "Total Users",
      value: stats?.total_users || "0",
      description: "Registered personnel",
      icon: Users,
      color: "text-blue-500",
    },
    {
      title: user.role === "regional" ? "Districts" : "Branches",
      value:
        user.role === "regional" ? "8" : user.role === "district" ? "3" : "1",
      description:
        user.role === "regional" ? "District branches" : "Local branches",
      icon: Building,
      color: "text-green-500",
    },
    {
      title: "Response Time",
      value: "4.2m",
      description: "Average response time",
      icon: Activity,
      color: "text-orange-500",
    },
  ];

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome back, {user.full_name}. Here's what's happening in your{" "}
              {user.department_display}.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {dashboardStats.map((stat, index) => (
              <Card key={index}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground">
                    {stat.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bell className="h-5 w-5" />
                  Recent Alerts
                </CardTitle>
                <CardDescription>
                  Latest emergency situations in your area
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {stats?.recent_alerts?.map((alert) => (
                    <div
                      key={alert.id}
                      className="flex items-center justify-between p-3 border rounded-lg"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              alert.priority === "high"
                                ? "destructive"
                                : alert.priority === "medium"
                                ? "default"
                                : "secondary"
                            }
                          >
                            {alert.priority}
                          </Badge>
                          <span className="font-medium">{alert.title}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {alert.location}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(alert.created_at).toLocaleString()}
                        </p>
                      </div>
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
                  )) || (
                    <p className="text-muted-foreground">No recent alerts</p>
                  )}
                </div>
                <div className="mt-4">
                  <Link href="/dashboard/alerts">
                    <Button variant="outline" className="w-full">
                      View All Alerts
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>Common tasks for your role</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link href="/dashboard/alerts/new">
                  <Button className="w-full justify-start" variant="outline">
                    <Plus className="h-4 w-4 mr-2" />
                    Create New Alert
                  </Button>
                </Link>

                {user.role === "regional" && (
                  <Link href="/dashboard/districts">
                    <Button className="w-full justify-start" variant="outline">
                      <Building className="h-4 w-4 mr-2" />
                      Manage Districts
                    </Button>
                  </Link>
                )}

                {(user.role === "regional" || user.role === "district") && (
                  <Link href="/dashboard/users">
                    <Button className="w-full justify-start" variant="outline">
                      <Users className="h-4 w-4 mr-2" />
                      Manage Users
                    </Button>
                  </Link>
                )}

                <Link href="/dashboard/history">
                  <Button className="w-full justify-start" variant="outline">
                    <History className="h-4 w-4 mr-2" />
                    View History
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
