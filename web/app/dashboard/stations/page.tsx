"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/dashboard-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataTable } from "@/components/ui/data-table";
import { StatsGrid } from "@/components/ui/stats-card";
import {
  Building,
  Search,
  Filter,
  MapPin,
  Users,
  Phone,
  Calendar,
  Eye,
  Edit,
  Trash2,
  Plus,
} from "lucide-react";

interface Station {
  station_id: string;
  name: string;
  code: string;
  station_type: string;
  department: string;
  region: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  latitude?: number;
  longitude?: number;
  manager_id?: string;
  manager?: {
    full_name: string;
    email: string;
    phone_number: string;
  };
  phone: string;
  description: string;
  capacity: number;
  operating_hours: string;
  is_active: boolean;
  established_date?: string;
  created_at: string;
  staff_count?: number;
}

export default function StationsPage() {
  const [user, setUser] = useState(null);
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      fetchStations();
    }
  }, []);

  const fetchStations = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/geography/stations/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setStations(data);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching stations:", error);
    } finally {
      setLoading(false);
    }
  };

  const getStationTypeColor = (type: string) => {
    switch (type) {
      case "headquarters":
        return "bg-blue-100 text-blue-800";
      case "substation":
        return "bg-green-100 text-green-800";
      case "outpost":
        return "bg-yellow-100 text-yellow-800";
      case "mobile":
        return "bg-purple-100 text-purple-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getDepartmentColor = (department: string) => {
    switch (department) {
      case "fire":
        return "bg-red-100 text-red-800";
      case "police":
        return "bg-blue-100 text-blue-800";
      case "medical":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  // Define columns for the DataTable
  const columns = [
    {
      key: "name",
      header: "Station",
      sortable: true,
      render: (station: Station) => (
        <div>
          <div className="font-medium">{station.name}</div>
          <div className="text-sm text-muted-foreground">{station.code}</div>
          <div className="text-xs text-muted-foreground flex items-center gap-1">
            <MapPin className="h-3 w-3" />
            {station.city}, {station.state}
          </div>
        </div>
      ),
    },
    {
      key: "station_type",
      header: "Type",
      render: (station: Station) => (
        <Badge className={getStationTypeColor(station.station_type)}>
          {station.station_type}
        </Badge>
      ),
    },
    {
      key: "department",
      header: "Department",
      render: (station: Station) => (
        <Badge className={getDepartmentColor(station.department || "unknown")}>
          {station.department || "N/A"}
        </Badge>
      ),
    },
    {
      key: "region",
      header: "Region",
      render: (station: Station) => station.region || "N/A",
    },
    {
      key: "manager",
      header: "Manager",
      render: (station: Station) =>
        station.manager ? (
          <div>
            <div className="font-medium">{station.manager.full_name}</div>
            <div className="text-sm text-muted-foreground">
              {station.manager.email}
            </div>
          </div>
        ) : (
          <span className="text-muted-foreground">No manager assigned</span>
        ),
    },
    {
      key: "staff",
      header: "Staff",
      render: (station: Station) => (
        <div className="text-center">
          <div className="font-medium">{station.staff_count || 0}</div>
          <div className="text-xs text-muted-foreground">
            / {station.capacity}
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (station: Station) => (
        <Badge variant={station.is_active ? "default" : "secondary"}>
          {station.is_active ? "Active" : "Inactive"}
        </Badge>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (station: Station) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm">
            <Eye className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Edit className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
    },
  ];

  // Define filters for the DataTable
  const filters = [
    {
      key: "department",
      label: "Department",
      options: [
        { value: "fire", label: "Fire Department" },
        { value: "police", label: "Police Department" },
        { value: "medical", label: "Medical Department" },
      ],
      filterFn: (station: Station, filterValue: string) =>
        station.department === filterValue,
    },
    {
      key: "region",
      label: "Region",
      options: [
        { value: "central", label: "Central Region" },
        { value: "north", label: "Northern Region" },
        { value: "southern", label: "Southern Region" },
      ],
      filterFn: (station: Station, filterValue: string) =>
        station.region === filterValue,
    },
    {
      key: "is_active",
      label: "Status",
      options: [
        { value: "true", label: "Active" },
        { value: "false", label: "Inactive" },
      ],
      filterFn: (station: Station, filterValue: string) =>
        String(station.is_active) === filterValue,
    },
  ];

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Stations</h1>
            <p className="text-muted-foreground">
              Manage emergency response stations across all regions
            </p>
          </div>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Add Station
          </Button>
        </div>

        {/* Stats Cards */}
        <StatsGrid
          stats={[
            {
              title: "Total Stations",
              value: stations.length,
              icon: Building,
              description: "All registered stations",
            },
            {
              title: "Active Stations",
              value: stations.filter((s) => s.is_active).length,
              icon: Building,
              description: "Currently operational",
            },
            {
              title: "Total Staff",
              value: stations.reduce((sum, s) => sum + (s.staff_count || 0), 0),
              icon: Users,
              description: "All station personnel",
            },
            {
              title: "Total Capacity",
              value: stations.reduce((sum, s) => sum + s.capacity, 0),
              icon: Users,
              description: "Maximum personnel capacity",
            },
          ]}
        />

        {/* Stations Table with built-in filters */}

        <DataTable
          data={stations}
          columns={columns}
          filters={filters}
          searchPlaceholder="Search stations..."
          searchKeys={["name", "code", "address"]}
          loading={loading}
          emptyMessage="No stations found"
          title={`Stations (${stations.length})`}
          pageSize={10}
        />
      </div>
    </DashboardLayout>
  );
}
