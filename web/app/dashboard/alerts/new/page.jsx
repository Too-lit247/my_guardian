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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { AlertTriangle, Save, ArrowLeft } from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function NewAlertPage() {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    alert_type: "",
    location: "",
    description: "",
    priority: "",
    assigned_to: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      router.push("/");
      return;
    }
    setUser(JSON.parse(userData));
  }, [router]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/alerts/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        router.push("/dashboard/alerts");
      } else {
        const data = await response.json();
        setError(data.message || "Failed to create alert");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  if (!user) return <div>Loading...</div>;

  const alertTypes = {
    fire: [
      { value: "building_fire", label: "Building Fire" },
      { value: "wildfire", label: "Wildfire" },
      { value: "gas_leak", label: "Gas Leak" },
      { value: "explosion", label: "Explosion" },
      { value: "hazmat_incident", label: "Hazmat Incident" },
    ],
    police: [
      { value: "robbery", label: "Robbery" },
      { value: "assault", label: "Assault" },
      { value: "traffic_violation", label: "Traffic Violation" },
      { value: "domestic_dispute", label: "Domestic Dispute" },
      { value: "suspicious_activity", label: "Suspicious Activity" },
    ],
    medical: [
      { value: "heart_attack", label: "Heart Attack" },
      { value: "traffic_accident", label: "Traffic Accident" },
      { value: "overdose", label: "Overdose" },
      { value: "fall_injury", label: "Fall Injury" },
      { value: "allergic_reaction", label: "Allergic Reaction" },
    ],
  };

  const teams = {
    fire: [
      "Fire Team Alpha",
      "Fire Team Beta",
      "Fire Team Gamma",
      "Hazmat Unit",
    ],
    police: ["Police Unit 1", "Police Unit 2", "Police Unit 3", "SWAT Team"],
    medical: [
      "Ambulance Unit 1",
      "Ambulance Unit 2",
      "Ambulance Unit 3",
      "Emergency Response Team",
    ],
  };

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <Link href="/dashboard/alerts">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Alerts
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold">Create New Alert</h1>
              <p className="text-muted-foreground">
                Report a new emergency situation
              </p>
            </div>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-red-500" />
                Emergency Alert Details
              </CardTitle>
              <CardDescription>
                Fill in the details of the emergency situation. All fields are
                required.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {error && (
                <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="title">Alert Title</Label>
                    <Input
                      id="title"
                      placeholder="Brief description of the emergency"
                      value={formData.title}
                      onChange={(e) =>
                        handleInputChange("title", e.target.value)
                      }
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="alert_type">Alert Type</Label>
                    <Select
                      value={formData.alert_type}
                      onValueChange={(value) =>
                        handleInputChange("alert_type", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select alert type" />
                      </SelectTrigger>
                      <SelectContent>
                        {alertTypes[user.department]?.map((type) => (
                          <SelectItem key={type.value} value={type.value}>
                            {type.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    placeholder="Exact address or location of the emergency"
                    value={formData.location}
                    onChange={(e) =>
                      handleInputChange("location", e.target.value)
                    }
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    placeholder="Detailed description of the emergency situation"
                    value={formData.description}
                    onChange={(e) =>
                      handleInputChange("description", e.target.value)
                    }
                    rows={4}
                    required
                  />
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="priority">Priority Level</Label>
                    <Select
                      value={formData.priority}
                      onValueChange={(value) =>
                        handleInputChange("priority", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select priority" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="high">
                          High - Immediate Response Required
                        </SelectItem>
                        <SelectItem value="medium">
                          Medium - Urgent Response
                        </SelectItem>
                        <SelectItem value="low">
                          Low - Standard Response
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="assigned_to">Assign To</Label>
                    <Select
                      value={formData.assigned_to}
                      onValueChange={(value) =>
                        handleInputChange("assigned_to", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select team/unit" />
                      </SelectTrigger>
                      <SelectContent>
                        {teams[user.department]?.map((team) => (
                          <SelectItem key={team} value={team}>
                            {team}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="flex gap-4 pt-4">
                  <Button type="submit" className="flex-1" disabled={loading}>
                    <Save className="h-4 w-4 mr-2" />
                    {loading ? "Creating..." : "Create Alert"}
                  </Button>
                  <Link href="/dashboard/alerts">
                    <Button type="button" variant="outline">
                      Cancel
                    </Button>
                  </Link>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
