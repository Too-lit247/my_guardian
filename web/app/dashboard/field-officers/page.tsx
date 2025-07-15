"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/dashboard-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { DataTable } from "@/components/ui/data-table";
import { StatsGrid } from "@/components/ui/stats-card";
import {
  Users,
  Plus,
  Eye,
  Edit,
  Trash2,
  Mail,
  Phone,
  Building,
  Shield,
  Flame,
  Heart,
} from "lucide-react";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

interface FieldOfficer {
  id: string;
  username: string;
  email: string;
  full_name: string;
  phone_number?: string;
  department: string;
  region: string;
  station_id?: string;
  role: string;
  is_active: boolean;
  is_active_user: boolean;
  created_at: string;
  last_login?: string;
}

export default function FieldOfficersPage() {
  const [user, setUser] = useState(null);
  const [fieldOfficers, setFieldOfficers] = useState<FieldOfficer[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      // Allow Station Managers and Admins to access this page
      if (!["Admin", "Station Manager"].includes(parsedUser.role)) {
        router.push("/dashboard");
        return;
      }
      
      fetchFieldOfficers();
    }
  }, []);

  const fetchFieldOfficers = async () => {
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
        const officers = data.results?.filter(
          (u: FieldOfficer) => u.role === "Field Officer"
        ) || [];
        setFieldOfficers(officers);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching field officers:", error);
    } finally {
      setLoading(false);
    }
  };

  const getDepartmentIcon = (department: string) => {
    switch (department) {
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
      key: "full_name",
      header: "Officer",
      sortable: true,
      render: (officer: FieldOfficer) => (
        <div className="flex items-center space-x-3">
          {getDepartmentIcon(officer.department)}
          <div>
            <div className="font-medium">{officer.full_name}</div>
            <div className="text-sm text-muted-foreground">{officer.username}</div>
          </div>
        </div>
      ),
    },
    {
      key: "email",
      header: "Contact",
      render: (officer: FieldOfficer) => (
        <div>
          <div className="flex items-center gap-1">
            <Mail className="h-3 w-3 text-muted-foreground" />
            <span className="text-sm">{officer.email}</span>
          </div>
          {officer.phone_number && (
            <div className="flex items-center gap-1 mt-1">
              <Phone className="h-3 w-3 text-muted-foreground" />
              <span className="text-sm">{officer.phone_number}</span>
            </div>
          )}
        </div>
      ),
    },
    {
      key: "department",
      header: "Department",
      render: (officer: FieldOfficer) => (
        <Badge className={getDepartmentColor(officer.department)}>
          {officer.department}
        </Badge>
      ),
    },
    {
      key: "region",
      header: "Region",
      render: (officer: FieldOfficer) => officer.region,
    },
    {
      key: "station_id",
      header: "Station",
      render: (officer: FieldOfficer) => (
        <div className="flex items-center gap-1">
          <Building className="h-3 w-3 text-muted-foreground" />
          <span className="text-sm">
            {officer.station_id ? officer.station_id : "Unassigned"}
          </span>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (officer: FieldOfficer) => (
        <div className="space-y-1">
          <Badge variant={officer.is_active ? "default" : "secondary"}>
            {officer.is_active ? "Active" : "Inactive"}
          </Badge>
          {officer.is_active_user && (
            <Badge variant="outline" className="text-green-600 border-green-300">
              Verified
            </Badge>
          )}
        </div>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (officer: FieldOfficer) => (
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
    },
    {
      key: "region",
      label: "Region",
      options: [
        { value: "central", label: "Central Region" },
        { value: "north", label: "Northern Region" },
        { value: "southern", label: "Southern Region" },
      ],
    },
    {
      key: "is_active",
      label: "Status",
      options: [
        { value: "true", label: "Active" },
        { value: "false", label: "Inactive" },
      ],
      filterFn: (officer: FieldOfficer, filterValue: string) => 
        String(officer.is_active) === filterValue,
    },
  ];

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
                Field Officers
              </h1>
              <p className="text-muted-foreground">
                Manage field officers and their assignments
              </p>
            </div>
            <Button asChild>
              <Link href="/dashboard/field-officers/new">
                <Plus className="h-4 w-4 mr-2" />
                Add Field Officer
              </Link>
            </Button>
          </div>

          {/* Stats Cards */}
          <StatsGrid
            stats={[
              {
                title: "Total Officers",
                value: fieldOfficers.length,
                icon: Users,
                description: "All field officers",
              },
              {
                title: "Active Officers",
                value: fieldOfficers.filter((o) => o.is_active).length,
                icon: Users,
                description: "Currently active",
              },
              {
                title: "Verified Officers",
                value: fieldOfficers.filter((o) => o.is_active_user).length,
                icon: Users,
                description: "Email verified",
              },
              {
                title: "Assigned Officers",
                value: fieldOfficers.filter((o) => o.station_id).length,
                icon: Building,
                description: "Assigned to stations",
              },
            ]}
          />

          {/* Field Officers Table */}
          <DataTable
            data={fieldOfficers}
            columns={columns}
            filters={filters}
            searchPlaceholder="Search field officers..."
            searchKeys={["full_name", "email", "username"]}
            loading={loading}
            emptyMessage="No field officers found"
            title={`Field Officers (${fieldOfficers.length})`}
            pageSize={10}
          />
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
