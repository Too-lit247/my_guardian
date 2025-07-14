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

export default function CreateDistrictPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    code: "",
    address: "",
    city: "",
    state: "",
    zip_code: "",
    phone: "",
    description: "",
    coverage_area: "",
    population_served: 0,
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/geography/districts/create/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...formData,
            // Don't send region and department - the backend sets these automatically
          }),
        }
      );
      console.log(await response.json());

      if (response.ok) {
        router.push("/dashboard/regional");
      } else {
        const errorData = await response.json();
        console.error("Failed to create district:", errorData);
        alert("Failed to create district. Please try again.");
      }
    } catch (error) {
      console.error("Error creating district:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
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
              onClick={() => router.push("/dashboard/regional")}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Regional Dashboard
            </Button>
            <div>
              <h1 className="text-3xl font-bold">Create New District</h1>
              <p className="text-muted-foreground">
                Add a new district to your {user.department} department region
              </p>
            </div>
          </div>

          <Card className="max-w-4xl">
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
                      placeholder="e.g., Central District"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="code">District Code *</Label>
                    <Input
                      id="code"
                      name="code"
                      value={formData.code}
                      onChange={handleInputChange}
                      placeholder="e.g., CD001"
                      maxLength={10}
                      required
                    />
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="city">City *</Label>
                    <Input
                      id="city"
                      name="city"
                      value={formData.city}
                      onChange={handleInputChange}
                      placeholder="Enter city name"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="population_served">Population Served</Label>
                    <Input
                      id="population_served"
                      name="population_served"
                      type="number"
                      value={formData.population_served}
                      onChange={handleInputChange}
                      placeholder="0"
                      min="0"
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
                    placeholder="Enter district headquarters address"
                    required
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                  <div className="space-y-2">
                    <Label htmlFor="state">State/Province</Label>
                    <Input
                      id="state"
                      name="state"
                      value={formData.state}
                      onChange={handleInputChange}
                      placeholder="Enter state/province"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="zip_code">ZIP/Postal Code</Label>
                    <Input
                      id="zip_code"
                      name="zip_code"
                      value={formData.zip_code}
                      onChange={handleInputChange}
                      placeholder="Enter ZIP code"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Contact Phone</Label>
                    <Input
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="+265991234567"
                      type="tel"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="coverage_area">Coverage Area</Label>
                  <Textarea
                    id="coverage_area"
                    name="coverage_area"
                    value={formData.coverage_area}
                    onChange={handleInputChange}
                    placeholder="Describe the geographical area this district covers"
                    rows={3}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Additional notes about this district"
                    rows={3}
                  />
                </div>

                <div className="flex gap-4 pt-4">
                  <Button type="submit" disabled={loading} className="flex-1">
                    <Save className="h-4 w-4 mr-2" />
                    {loading ? "Creating District..." : "Create District"}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => router.push("/dashboard/regional")}
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
