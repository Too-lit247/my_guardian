"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  User,
  Building,
  MapPin,
  FileText,
  CheckCircle,
  XCircle,
  ArrowLeft,
  Shield,
  Flame,
  Heart,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";
import Link from "next/link";

export default function RequestReviewPage() {
  const [user, setUser] = useState(null);
  const [request, setRequest] = useState(null);
  const [reviewNotes, setReviewNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const router = useRouter();
  const params = useParams();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);

      if (parsedUser.role !== "Admin") {
        router.push("/dashboard");
        return;
      }

      fetchRequest();
    }
  }, []);

  const fetchRequest = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/registration-requests/${params.id}/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setRequest(data);
      } else {
        router.push("/dashboard/admin");
      }
    } catch (error) {
      console.error("Error fetching request:", error);
      router.push("/dashboard/admin");
    } finally {
      setLoading(false);
    }
  };

  const handleReview = async (status) => {
    setSubmitting(true);
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/registration-requests/${params.id}/review/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            status,
            review_notes: reviewNotes,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        router.push("/dashboard/admin");
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Failed to review request");
      }
    } catch (error) {
      console.error("Error reviewing request:", error);
      alert("Network error occurred");
    } finally {
      setSubmitting(false);
    }
  };

  const getDepartmentIcon = (dept) => {
    switch (dept) {
      case "fire":
        return <Flame className="h-5 w-5 text-red-500" />;
      case "police":
        return <Shield className="h-5 w-5 text-blue-500" />;
      case "medical":
        return <Heart className="h-5 w-5 text-green-500" />;
      default:
        return <User className="h-5 w-5 text-gray-500" />;
    }
  };

  if (!user || loading) {
    return <div>Loading...</div>;
  }

  if (!request) {
    return <div>Request not found</div>;
  }

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm" asChild>
                <Link href="/dashboard/admin">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Admin
                </Link>
              </Button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Review Registration Request
                </h1>
                <p className="text-muted-foreground">
                  Request ID: {request.request_id}
                </p>
              </div>
            </div>
            <Badge
              variant={request.status === "pending" ? "outline" : "default"}
            >
              {request.status}
            </Badge>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Request Details */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="h-5 w-5" />
                    Registration Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium">
                      Registration Type
                    </Label>
                    <p className="text-sm capitalize">
                      {request.registration_type}
                    </p>
                  </div>
                  {request.organization_name && (
                    <div>
                      <Label className="text-sm font-medium">
                        Organization Name
                      </Label>
                      <p className="text-sm">{request.organization_name}</p>
                    </div>
                  )}
                  <div>
                    <Label className="text-sm font-medium">Department</Label>
                    <div className="flex items-center gap-2 mt-1">
                      {getDepartmentIcon(request.department)}
                      <span className="text-sm capitalize">
                        {request.department} Department
                      </span>
                    </div>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Region</Label>
                    <p className="text-sm">
                      {request.region === "central"
                        ? "Central"
                        : request.region === "north"
                        ? "Northern"
                        : "Southern"}{" "}
                      Region
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <User className="h-5 w-5" />
                    Personal Details
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium">Full Name</Label>
                    <p className="text-sm">{request.full_name}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Email</Label>
                    <p className="text-sm">{request.email}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium">Phone Number</Label>
                    <p className="text-sm">{request.phone_number}</p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MapPin className="h-5 w-5" />
                    Location Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="text-sm font-medium">Address</Label>
                    <p className="text-sm">{request.address}</p>
                  </div>
                  {request.latitude && request.longitude && (
                    <div>
                      <Label className="text-sm font-medium">Coordinates</Label>
                      <p className="text-sm">
                        {request.latitude}, {request.longitude}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {request.documentation && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      Documentation
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" size="sm" asChild>
                      <a
                        href={request.documentation}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View Document
                      </a>
                    </Button>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Review Section */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Review Request</CardTitle>
                  <CardDescription>
                    Add your review notes and approve or deny this registration
                    request
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="review_notes">Review Notes</Label>
                    <Textarea
                      id="review_notes"
                      placeholder="Add any notes about your decision..."
                      value={reviewNotes}
                      onChange={(e) => setReviewNotes(e.target.value)}
                      rows={4}
                      className="mt-1"
                    />
                  </div>

                  {request.status === "pending" && (
                    <div className="flex space-x-3">
                      <Button
                        onClick={() => handleReview("approved")}
                        disabled={submitting}
                        className="flex-1 bg-green-600 hover:bg-green-700"
                      >
                        <CheckCircle className="h-4 w-4 mr-2" />
                        {submitting ? "Processing..." : "Approve"}
                      </Button>
                      <Button
                        onClick={() => handleReview("denied")}
                        disabled={submitting}
                        variant="destructive"
                        className="flex-1"
                      >
                        <XCircle className="h-4 w-4 mr-2" />
                        {submitting ? "Processing..." : "Deny"}
                      </Button>
                    </div>
                  )}

                  {request.status !== "pending" && (
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm font-medium">
                        Request Status: {request.status}
                      </p>
                      {request.reviewed_by_name && (
                        <p className="text-sm text-muted-foreground">
                          Reviewed by: {request.reviewed_by_name}
                        </p>
                      )}
                      {request.review_notes && (
                        <div className="mt-2">
                          <p className="text-sm font-medium">Review Notes:</p>
                          <p className="text-sm text-muted-foreground">
                            {request.review_notes}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Request Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <div>
                        <p className="text-sm font-medium">Request Submitted</p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(request.created_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    {request.reviewed_at && (
                      <div className="flex items-center space-x-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <div>
                          <p className="text-sm font-medium">
                            Request Reviewed
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {new Date(request.reviewed_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
