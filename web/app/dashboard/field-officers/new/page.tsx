"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/dashboard-layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, UserPlus, Mail, Phone, Building } from "lucide-react";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

interface Station {
  station_id: string;
  name: string;
  code: string;
  department: string;
  region: string;
}

export default function NewFieldOfficerPage() {
  const [user, setUser] = useState(null);
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone_number: "",
    department: "",
    region: "",
    station_id: "",
    notes: "",
  });
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
        setStations(data || []);
      }
    } catch (error) {
      console.error("Error fetching stations:", error);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");

      // Prepare form data, converting "none" station_id to empty string
      const submitData = {
        ...formData,
        station_id: formData.station_id === "none" ? "" : formData.station_id,
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/field-officers/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(submitData),
        }
      );

      if (response.ok) {
        const data = await response.json();
        alert(
          "Field officer created successfully! Email sent with login credentials."
        );
        router.push("/dashboard/field-officers");
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Failed to create field officer");
      }
    } catch (error) {
      console.error("Error creating field officer:", error);
      alert("An error occurred while creating the field officer");
    } finally {
      setLoading(false);
    }
  };

  const departmentOptions = [
    { value: "fire", label: "Fire Department" },
    { value: "police", label: "Police Department" },
    { value: "medical", label: "Medical Department" },
  ];

  const regionOptions = [
    { value: "central", label: "Central Region" },
    { value: "north", label: "Northern Region" },
    { value: "southern", label: "Southern Region" },
  ];

  // Filter stations based on selected department and region
  const filteredStations = stations.filter((station) => {
    if (formData.department && station.department !== formData.department) {
      return false;
    }
    if (formData.region && station.region !== formData.region) {
      return false;
    }
    return true;
  });

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard/field-officers">
                <ArrowLeft className="h-4 w-4" />
              </Link>
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Add New Field Officer
              </h1>
              <p className="text-muted-foreground">
                Create a new field officer account with automatic email
                notification
              </p>
            </div>
          </div>

          {/* Form */}
          <Card className="max-w-2xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UserPlus className="h-5 w-5" />
                Field Officer Information
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Personal Information */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Personal Information</h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="full_name">Full Name *</Label>
                      <Input
                        id="full_name"
                        value={formData.full_name}
                        onChange={(e) =>
                          handleInputChange("full_name", e.target.value)
                        }
                        placeholder="Enter full name"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address *</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="email"
                          type="email"
                          value={formData.email}
                          onChange={(e) =>
                            handleInputChange("email", e.target.value)
                          }
                          placeholder="Enter email address"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="phone_number">Phone Number</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="phone_number"
                        value={formData.phone_number}
                        onChange={(e) =>
                          handleInputChange("phone_number", e.target.value)
                        }
                        placeholder="Enter phone number"
                        className="pl-10"
                      />
                    </div>
                  </div>
                </div>

                {/* Assignment Information */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium">
                    Assignment Information
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="department">Department *</Label>
                      <Select
                        value={formData.department}
                        onValueChange={(value) =>
                          handleInputChange("department", value)
                        }
                        required
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select department" />
                        </SelectTrigger>
                        <SelectContent>
                          {departmentOptions.map((option) => (
                            <SelectItem key={option.value} value={option.value}>
                              {option.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="region">Region *</Label>
                      <Select
                        value={formData.region}
                        onValueChange={(value) =>
                          handleInputChange("region", value)
                        }
                        required
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select region" />
                        </SelectTrigger>
                        <SelectContent>
                          {regionOptions.map((option) => (
                            <SelectItem key={option.value} value={option.value}>
                              {option.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="station_id">Assign to Station</Label>
                    <div className="relative">
                      <Building className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Select
                        value={formData.station_id}
                        onValueChange={(value) =>
                          handleInputChange("station_id", value)
                        }
                      >
                        <SelectTrigger className="pl-10">
                          <SelectValue placeholder="Select station (optional)" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="none">
                            No station assignment
                          </SelectItem>
                          {filteredStations.map((station) => (
                            <SelectItem
                              key={station.station_id}
                              value={station.station_id}
                            >
                              {station.name} ({station.code})
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Select department and region first to see available
                      stations
                    </p>
                  </div>
                </div>

                {/* Additional Notes */}
                <div className="space-y-2">
                  <Label htmlFor="notes">Additional Notes</Label>
                  <Textarea
                    id="notes"
                    value={formData.notes}
                    onChange={(e) => handleInputChange("notes", e.target.value)}
                    placeholder="Any additional information about this field officer..."
                    rows={3}
                  />
                </div>

                {/* Submit Button */}
                <div className="flex items-center gap-4 pt-4">
                  <Button type="submit" disabled={loading}>
                    {loading ? "Creating..." : "Create Field Officer"}
                  </Button>
                  <Button type="button" variant="outline" asChild>
                    <Link href="/dashboard/field-officers">Cancel</Link>
                  </Button>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-800">
                    <strong>Note:</strong> A random password will be generated
                    for this field officer. They will receive an email with
                    their login credentials and can change their password after
                    first login.
                  </p>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
