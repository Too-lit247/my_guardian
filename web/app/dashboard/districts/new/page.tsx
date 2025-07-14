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
import { ArrowLeft, Building, Save } from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";

interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: string;
  department: string;
  region: string;
}

export default function NewDistrictPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    address: "",
    manager: "",
    description: "",
    contact_phone: "",
    contact_email: "",
  });
  const router = useRouter();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      router.push("/");
      return;
    }
    const currentUser = JSON.parse(userData);
    setUser(currentUser);

    // Only regional managers can access this page
    if (currentUser.role !== "Regional Manager") {
      router.push("/dashboard");
      return;
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/geography/districts/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...formData,
            region: user?.region,
            department: user?.department,
          }),
        }
      );

      if (response.ok) {
        router.push("/dashboard/districts");
      } else {
        console.error("Failed to create district");
      }
    } catch (error) {
      console.error("Error creating district:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  if (!user) return <div>Loading...</div>;

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.back()}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-3xl font-bold">Create New District</h1>
              <p className="text-muted-foreground">
                Add a new district branch to your {user.department} department region
              </p>
            </div>
          </div>

          <Card className="max-w-2xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building className="h-5 w-5" />
                District Information
              </CardTitle>
              <CardDescription>
                Enter the details for the new district branch
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="name">District Name *</Label>
                    <Input
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="Enter district name"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="manager">District Manager *</Label>
                    <Input
                      id="manager"
                      name="manager"
                      value={formData.manager}
                      onChange={handleInputChange}
                      placeholder="Enter manager name"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="address">Address *</Label>
                  <Input
                    id="address"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    placeholder="Enter district address"
                    required
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="contact_phone">Contact Phone</Label>
                    <Input
                      id="contact_phone"
                      name="contact_phone"
                      value={formData.contact_phone}
                      onChange={handleInputChange}
                      placeholder="+265991234567"
                      type="tel"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="contact_email">Contact Email</Label>
                    <Input
                      id="contact_email"
                      name="contact_email"
                      value={formData.contact_email}
                      onChange={handleInputChange}
                      placeholder="district@example.com"
                      type="email"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Enter district description and coverage area"
                    rows={4}
                  />
                </div>

                <div className="flex gap-4 pt-4">
                  <Button type="submit" disabled={loading} className="flex-1">
                    <Save className="h-4 w-4 mr-2" />
                    {loading ? "Creating..." : "Create District"}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => router.back()}
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
