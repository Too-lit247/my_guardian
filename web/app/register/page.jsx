"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  User,
  Building,
  MapPin,
  Upload,
  CheckCircle,
  ArrowLeft,
  ArrowRight,
  Shield,
  Flame,
  Heart,
  Users,
} from "lucide-react";
import { useRouter } from "next/navigation";

const steps = [
  { id: 1, title: "Registration Type", icon: User },
  { id: 2, title: "Organization Details", icon: Building },
  { id: 3, title: "Location", icon: MapPin },
  { id: 4, title: "Documentation", icon: Upload },
  { id: 5, title: "Personal Details", icon: User },
  { id: 6, title: "Review & Submit", icon: CheckCircle },
];

export default function RegisterPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    registration_type: "",
    organization_name: "",
    department: "",
    region: "",
    full_name: "",
    email: "",
    phone_number: "",
    latitude: null,
    longitude: null,
    address: "",
    documentation: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const progress = (currentStep / steps.length) * 100;

  const getDepartmentIcon = (dept) => {
    switch (dept) {
      case "fire":
        return <Flame className="h-5 w-5 text-red-500" />;
      case "police":
        return <Shield className="h-5 w-5 text-blue-500" />;
      case "medical":
        return <Heart className="h-5 w-5 text-green-500" />;
      default:
        return <Users className="h-5 w-5 text-gray-500" />;
    }
  };

  const getDepartmentColor = (dept) => {
    switch (dept) {
      case "fire":
        return "bg-red-50 border-red-200 text-red-700";
      case "police":
        return "bg-blue-50 border-blue-200 text-blue-700";
      case "medical":
        return "bg-green-50 border-green-200 text-green-700";
      default:
        return "bg-gray-50 border-gray-200 text-gray-700";
    }
  };

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      const formDataToSend = new FormData();
      Object.keys(formData).forEach((key) => {
        if (formData[key] !== null && formData[key] !== "") {
          formDataToSend.append(key, formData[key]);
        }
      });

      const response = await fetch(
        `${process.env.BACKEND_URL}/auth/registration-request/`,
        {
          method: "POST",
          body: formDataToSend,
        }
      );

      if (response.ok) {
        setSuccess(true);
      } else {
        const data = await response.json();
        setError(data.detail || "Registration failed");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">
                Choose Registration Type
              </h3>
              <p className="text-muted-foreground">
                Are you registering as an individual or organization?
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card
                className={`cursor-pointer transition-all hover:shadow-md ${
                  formData.registration_type === "individual"
                    ? "ring-2 ring-primary bg-primary/5"
                    : "hover:bg-gray-50"
                }`}
                onClick={() =>
                  setFormData({ ...formData, registration_type: "individual" })
                }
              >
                <CardContent className="p-6 text-center">
                  <User className="h-12 w-12 mx-auto mb-4 text-primary" />
                  <h4 className="font-semibold mb-2">Individual</h4>
                  <p className="text-sm text-muted-foreground">
                    Register as an individual responder
                  </p>
                </CardContent>
              </Card>
              <Card
                className={`cursor-pointer transition-all hover:shadow-md ${
                  formData.registration_type === "organization"
                    ? "ring-2 ring-primary bg-primary/5"
                    : "hover:bg-gray-50"
                }`}
                onClick={() =>
                  setFormData({
                    ...formData,
                    registration_type: "organization",
                  })
                }
              >
                <CardContent className="p-6 text-center">
                  <Building className="h-12 w-12 mx-auto mb-4 text-primary" />
                  <h4 className="font-semibold mb-2">Organization</h4>
                  <p className="text-sm text-muted-foreground">
                    Register as an emergency response organization
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">
                Organization Details
              </h3>
              <p className="text-muted-foreground">
                Tell us about your organization
              </p>
            </div>

            {formData.registration_type === "organization" && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="organization_name">Organization Name</Label>
                  <Input
                    id="organization_name"
                    value={formData.organization_name}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        organization_name: e.target.value,
                      })
                    }
                    placeholder="Enter organization name"
                    className="mt-1"
                  />
                </div>
              </div>
            )}

            <div>
              <Label htmlFor="department">Department</Label>
              <Select
                value={formData.department}
                onValueChange={(value) =>
                  setFormData({ ...formData, department: value })
                }
              >
                <SelectTrigger className="mt-1">
                  <SelectValue placeholder="Select department" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="fire">
                    <div className="flex items-center gap-2">
                      <Flame className="h-4 w-4 text-red-500" />
                      Fire Department
                    </div>
                  </SelectItem>
                  <SelectItem value="police">
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4 text-blue-500" />
                      Police Department
                    </div>
                  </SelectItem>
                  <SelectItem value="medical">
                    <div className="flex items-center gap-2">
                      <Heart className="h-4 w-4 text-green-500" />
                      Medical Department
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="region">Region</Label>
              <Select
                value={formData.region}
                onValueChange={(value) =>
                  setFormData({ ...formData, region: value })
                }
              >
                <SelectTrigger className="mt-1">
                  <SelectValue placeholder="Select region" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="central">Central Region</SelectItem>
                  <SelectItem value="north">Northern Region</SelectItem>
                  <SelectItem value="southern">Southern Region</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">
                Location Information
              </h3>
              <p className="text-muted-foreground">
                Provide your location details
              </p>
            </div>

            <div>
              <Label htmlFor="address">Address</Label>
              <Textarea
                id="address"
                value={formData.address}
                onChange={(e) =>
                  setFormData({ ...formData, address: e.target.value })
                }
                placeholder="Enter your full address"
                className="mt-1"
                rows={3}
              />
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <MapPin className="h-5 w-5 text-primary" />
                <span className="font-medium">Map Integration</span>
              </div>
              <p className="text-sm text-muted-foreground mb-3">
                Click on the map to set your precise location
              </p>
              <div className="bg-white border rounded-lg h-64 flex items-center justify-center">
                <div className="text-center text-muted-foreground">
                  <MapPin className="h-8 w-8 mx-auto mb-2" />
                  <p>OpenStreetMap integration will be added here</p>
                  <p className="text-xs mt-1">
                    For now, you can manually enter coordinates
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <Label htmlFor="latitude">Latitude</Label>
                  <Input
                    id="latitude"
                    type="number"
                    step="any"
                    value={formData.latitude || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        latitude: parseFloat(e.target.value),
                      })
                    }
                    placeholder="e.g., 40.7128"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="longitude">Longitude</Label>
                  <Input
                    id="longitude"
                    type="number"
                    step="any"
                    value={formData.longitude || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        longitude: parseFloat(e.target.value),
                      })
                    }
                    placeholder="e.g., -74.0060"
                    className="mt-1"
                  />
                </div>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">
                Upload Documentation
              </h3>
              <p className="text-muted-foreground">
                Upload documents that verify your organization
              </p>
            </div>

            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors">
              <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <div className="space-y-2">
                <p className="text-sm font-medium">
                  Upload certification documents
                </p>
                <p className="text-xs text-muted-foreground">
                  PDF or image files (max 10MB)
                </p>
              </div>
              <Input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) =>
                  setFormData({ ...formData, documentation: e.target.files[0] })
                }
                className="mt-4 max-w-xs mx-auto"
              />
              {formData.documentation && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm text-green-700">
                    ✓ {formData.documentation.name} uploaded
                  </p>
                </div>
              )}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Personal Details</h3>
              <p className="text-muted-foreground">
                Enter your personal information
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="full_name">Full Name</Label>
                <Input
                  id="full_name"
                  value={formData.full_name}
                  onChange={(e) =>
                    setFormData({ ...formData, full_name: e.target.value })
                  }
                  placeholder="Enter your full name"
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="phone_number">Phone Number</Label>
                <Input
                  id="phone_number"
                  value={formData.phone_number}
                  onChange={(e) =>
                    setFormData({ ...formData, phone_number: e.target.value })
                  }
                  placeholder="Enter your phone number"
                  className="mt-1"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                placeholder="Enter your email address"
                className="mt-1"
              />
              <p className="text-xs text-muted-foreground mt-1">
                This will be your username for logging in
              </p>
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Review & Submit</h3>
              <p className="text-muted-foreground">
                Please review your information before submitting
              </p>
            </div>

            <div className="space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <User className="h-4 w-4" />
                  Registration Type
                </h4>
                <p className="text-sm capitalize">
                  {formData.registration_type}
                </p>
                {formData.organization_name && (
                  <p className="text-sm font-medium mt-1">
                    {formData.organization_name}
                  </p>
                )}
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <Building className="h-4 w-4" />
                  Department & Region
                </h4>
                <div className="flex items-center gap-2 mb-2">
                  {getDepartmentIcon(formData.department)}
                  <span className="text-sm capitalize">
                    {formData.department} Department
                  </span>
                </div>
                <p className="text-sm">
                  {formData.region === "central"
                    ? "Central"
                    : formData.region === "north"
                    ? "Northern"
                    : "Southern"}{" "}
                  Region
                </p>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  Location
                </h4>
                <p className="text-sm">{formData.address}</p>
                {formData.latitude && formData.longitude && (
                  <p className="text-xs text-muted-foreground mt-1">
                    Coordinates: {formData.latitude}, {formData.longitude}
                  </p>
                )}
              </div>

              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <User className="h-4 w-4" />
                  Personal Information
                </h4>
                <div className="space-y-1 text-sm">
                  <p>
                    <span className="font-medium">Name:</span>{" "}
                    {formData.full_name}
                  </p>
                  <p>
                    <span className="font-medium">Email:</span> {formData.email}
                  </p>
                  <p>
                    <span className="font-medium">Phone:</span>{" "}
                    {formData.phone_number}
                  </p>
                </div>
              </div>

              {formData.documentation && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <Upload className="h-4 w-4" />
                    Documentation
                  </h4>
                  <p className="text-sm">✓ {formData.documentation.name}</p>
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <Card className="w-full max-w-md">
          <CardContent className="p-8 text-center">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Registration Submitted!
            </h2>
            <p className="text-muted-foreground mb-6">
              Your registration request has been submitted successfully. You
              will receive an email notification once it's reviewed.
            </p>
            <Button onClick={() => router.push("/")} className="w-full">
              Return to Login
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Organization Registration
            </h1>
            <p className="text-muted-foreground">
              Join the MyGuardian+ emergency response network
            </p>
          </div>

          {/* Progress Steps */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              {steps.map((step, index) => (
                <div key={step.id} className="flex flex-col items-center">
                  <div
                    className={`
                    w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
                    ${
                      currentStep >= step.id
                        ? "bg-primary text-white"
                        : "bg-gray-200 text-gray-500"
                    }
                  `}
                  >
                    {currentStep > step.id ? (
                      <CheckCircle className="h-5 w-5" />
                    ) : (
                      <step.icon className="h-5 w-5" />
                    )}
                  </div>
                  <span className="text-xs mt-1 text-center hidden sm:block">
                    {step.title}
                  </span>
                </div>
              ))}
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {/* Main Form */}
          <Card className="shadow-lg">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Badge variant="outline">
                  Step {currentStep} of {steps.length}
                </Badge>
                {formData.department && (
                  <Badge className={getDepartmentColor(formData.department)}>
                    {getDepartmentIcon(formData.department)}
                    <span className="ml-1 capitalize">
                      {formData.department}
                    </span>
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent className="p-6">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
                  {error}
                </div>
              )}

              {renderStep()}

              {/* Navigation */}
              <div className="flex justify-between mt-8">
                <Button
                  variant="outline"
                  onClick={handlePrevious}
                  disabled={currentStep === 1}
                  className="flex items-center gap-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Previous
                </Button>

                {currentStep < steps.length ? (
                  <Button
                    onClick={handleNext}
                    disabled={
                      (currentStep === 1 && !formData.registration_type) ||
                      (currentStep === 2 &&
                        (!formData.department ||
                          !formData.region ||
                          (formData.registration_type === "organization" &&
                            !formData.organization_name))) ||
                      (currentStep === 3 && !formData.address) ||
                      (currentStep === 5 &&
                        (!formData.full_name ||
                          !formData.email ||
                          !formData.phone_number))
                    }
                    className="flex items-center gap-2"
                  >
                    Next
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    onClick={handleSubmit}
                    disabled={
                      loading ||
                      !formData.full_name ||
                      !formData.email ||
                      !formData.phone_number
                    }
                    className="flex items-center gap-2"
                  >
                    {loading ? "Submitting..." : "Submit Registration"}
                    <CheckCircle className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
