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
import {
  Search,
  Plus,
  Eye,
  Edit,
  Trash2,
  AlertTriangle,
  CheckCircle,
  XCircle,
  MapPin,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

// User interface
interface User {
  id: string;
  email: string;
  role: string;
  department: string;
  station_id?: string;
  full_name: string;
}

// Alert interface
interface Alert {
  id: string;
  title: string;
  description: string;
  priority: string;
  status: string;
  department: string;
  alert_type?: string;
  assigned_station_id?: string;
  assigned_to?: string;
  location: string;
  latitude?: number;
  longitude?: number;
  created_at: string;
  updated_at: string;
}

// Emergency Trigger interface
interface EmergencyTrigger {
  trigger_id: string;
  device_info: {
    owner_name: string;
    owner_phone: string;
    serial_number: string;
  };
  trigger_type: string;
  severity: string;
  trigger_value: number;
  threshold_value: number;
  latitude: number | null;
  longitude: number | null;
  acknowledged: boolean;
  triggered_at: string;
}

export default function AlertsPage() {
  const [user, setUser] = useState<User | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [triggers, setTriggers] = useState<EmergencyTrigger[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      router.push("/");
      return;
    }
    setUser(JSON.parse(userData));
    fetchAlerts();
    fetchEmergencyTriggers();
  }, [router]);

  const fetchAlerts = async () => {
    try {
      let url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/alerts/`;
      const params = new URLSearchParams();

      if (statusFilter !== "all") params.append("status", statusFilter);
      if (priorityFilter !== "all") params.append("priority", priorityFilter);
      if (searchTerm) params.append("search", searchTerm);

      // Note: Station-based filtering is handled automatically by the backend
      // based on the authenticated user's role and station assignment

      if (params.toString()) {
        url += "?" + params.toString();
      }

      const token = localStorage.getItem("access_token");
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        setAlerts(data.results || data);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching alerts:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmergencyTriggers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/devices/triggers/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setTriggers(data.results || data);
      }
    } catch (error) {
      console.error("Error fetching emergency triggers:", error);
    }
  };

  const acknowledgeEmergencyTrigger = async (triggerId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/devices/triggers/${triggerId}/acknowledge/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        fetchEmergencyTriggers();
      }
    } catch (error) {
      console.error("Error acknowledging trigger:", error);
    }
  };

  useEffect(() => {
    if (user) {
      fetchAlerts();
    }
  }, [searchTerm, statusFilter, priorityFilter, user]);

  const deleteAlert = async (alertId: string) => {
    if (!confirm("Are you sure you want to delete this alert?")) return;

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/alerts/${alertId}/`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        fetchAlerts();
      }
    } catch (error) {
      console.error("Error deleting alert:", error);
    }
  };

  if (!user || loading) return <div>Loading...</div>;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "destructive";
      case "medium":
        return "default";
      case "low":
        return "secondary";
      default:
        return "secondary";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "destructive";
      case "in_progress":
        return "default";
      case "resolved":
        return "secondary";
      default:
        return "secondary";
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "destructive";
      case "high":
        return "destructive";
      case "medium":
        return "default";
      case "low":
        return "secondary";
      default:
        return "secondary";
    }
  };

  const unacknowledgedTriggers = triggers.filter((t) => !t.acknowledged);

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Emergency Alerts</h1>
              <p className="text-muted-foreground">
                {user &&
                ["Field Officer", "Station Manager"].includes(user.role) &&
                user.station_id
                  ? `Showing alerts for your station only`
                  : "Manage and monitor emergency situations"}
              </p>
            </div>
            <Link href="/dashboard/alerts/new">
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                New Alert
              </Button>
            </Link>
          </div>

          {/* Emergency Triggers Alert */}
          {unacknowledgedTriggers.length > 0 && (
            <Card className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-red-700">
                  <AlertTriangle className="h-5 w-5" />
                  Emergency Triggers ({unacknowledgedTriggers.length})
                </CardTitle>
                <CardDescription className="text-red-600">
                  Unacknowledged emergency situations detected by devices
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {unacknowledgedTriggers.slice(0, 5).map((trigger) => (
                    <div
                      key={trigger.trigger_id}
                      className="flex items-center justify-between p-3 bg-white border border-red-200 rounded"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Badge variant={getSeverityColor(trigger.severity)}>
                            {trigger.severity}
                          </Badge>
                          <span className="font-medium">
                            {trigger.trigger_type.replace("_", " ")}
                          </span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {trigger.device_info.owner_name} -{" "}
                          {trigger.device_info.serial_number}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(trigger.triggered_at).toLocaleString()}
                        </p>
                        {trigger.latitude && trigger.longitude && (
                          <div className="text-xs text-muted-foreground flex flex-col gap-1">
                            <p>
                              📍 {trigger.latitude}, {trigger.longitude}
                            </p>
                            <a
                              href={`https://www.google.com/maps?q=${trigger.latitude},${trigger.longitude}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline w-fit"
                            >
                              <MapPin className="h-4 w-4 inline mr-1" />
                              View in Maps
                            </a>
                          </div>
                        )}
                      </div>
                      <Button
                        size="sm"
                        onClick={() =>
                          acknowledgeEmergencyTrigger(trigger.trigger_id)
                        }
                      >
                        Acknowledge
                      </Button>
                    </div>
                  ))}
                  {unacknowledgedTriggers.length > 5 && (
                    <p className="text-sm text-muted-foreground text-center">
                      +{unacknowledgedTriggers.length - 5} more triggers
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle>Filters</CardTitle>
              <CardDescription>
                Filter alerts by status, priority, or search terms
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4 md:flex-row md:items-center">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search alerts..."
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
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="resolved">Resolved</SelectItem>
                  </SelectContent>
                </Select>
                <Select
                  value={priorityFilter}
                  onValueChange={setPriorityFilter}
                >
                  <SelectTrigger className="w-full md:w-[180px]">
                    <SelectValue placeholder="Filter by priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Priority</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Active Alerts ({alerts.length})</CardTitle>
              <CardDescription>
                Current emergency situations requiring attention
              </CardDescription>
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
                      <TableHead>Assigned To</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {alerts.map((alert) => (
                      <TableRow key={alert.id}>
                        <TableCell>
                          <div>
                            <div className="font-medium">{alert.title}</div>
                            <div className="text-sm text-muted-foreground">
                              {alert.alert_type}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">{alert.location}</div>
                        </TableCell>
                        <TableCell>
                          <Badge variant={getPriorityColor(alert.priority)}>
                            {alert.priority}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={getStatusColor(alert.status)}>
                            {alert.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {alert.assigned_to || "Unassigned"}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {new Date(alert.created_at).toLocaleDateString()}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-red-600 hover:text-red-700"
                              onClick={() => deleteAlert(alert.id)}
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
