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
import { Shield, Flame, Heart, AlertCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [loginData, setLoginData] = useState({
    username: "admin",
    password: "admin123",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    setLoading(true);
    setError("");

    console.log("Attempting login with:", loginData);

    try {
      const response = await fetch(`${process.env.BACKEND_URL}/auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginData),
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));
        router.push("/dashboard");
      } else {
        setError(data.detail || data.non_field_errors?.[0] || "Login failed");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError("Network error. Please check if the backend server is running.");
    } finally {
      setLoading(false);
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
      case "admin":
        return <Shield className="h-5 w-5 text-gray-800" />;
      default:
        return null;
    }
  };
  /*
  const loadSampleCredentials = (type) => {
    const credentials = {
      admin: {
        username: "admin",
        password: "admin123",
        department: "admin",
        role: "System Administrator",
      },
      fire: {
        username: "fire_regional_mw",
        password: "admin123",
        department: "fire",
        role: "Regional Manager",
      },
      police: {
        username: "police_regional_mw",
        password: "admin123",
        department: "police",
        role: "Regional Manager",
      },
      medical: {
        username: "medical_regional_mw",
        password: "admin123",
        department: "medical",
        role: "Regional Manager",
      },
    }
    setLoginData(credentials[type])
  }
*/
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">MyGuardian+</CardTitle>
          <CardDescription>
            Emergency Response Management System
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <div className="flex items-center gap-2 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={loginData.username}
              onChange={(e) =>
                setLoginData((prev) => ({
                  ...prev,
                  username: e.target.value,
                }))
              }
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={loginData.password}
              onChange={(e) =>
                setLoginData((prev) => ({
                  ...prev,
                  password: e.target.value,
                }))
              }
            />
          </div>

          <Button
            className="w-full"
            onClick={handleLogin}
            disabled={!loginData.username || !loginData.password || loading}
          >
            {loading ? "Signing In..." : "Sign In"}
          </Button>

          <div className="text-center">
            <p className="text-sm text-muted-foreground">
              Don't have an account?{" "}
              <Link
                href="/register"
                className="text-primary hover:underline font-medium"
              >
                Register your organization
              </Link>
            </p>
          </div>

          {/* <div className="text-center text-sm text-muted-foreground space-y-2">
                <p className="font-medium">Quick Login Options:</p>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("admin")}>
                    Admin
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("fire")}>
                    Fire Dept
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("police")}>
                    Police
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => loadSampleCredentials("medical")}>
                    Medical
                  </Button>
                </div>
                <p className="text-xs mt-2">
                  Default password for all accounts: <code>admin123</code>
                </p>
              </div> */}
        </CardContent>
      </Card>
    </div>
  );
}
