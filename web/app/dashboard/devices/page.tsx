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
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Smartphone,
  Battery,
  MapPin,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
} from "lucide-react";
import DashboardLayout from "@/components/dashboard-layout";
import AuthWrapper from "@/components/auth-wrapper";

interface Device {
  device_id: string;
  mac_address: string;
  serial_number: string;
  device_type: string;
  owner_name: string;
  owner_phone: string;
  owner_address: string;
  emergency_contact: string;
  emergency_contact_phone: string;
  medical_conditions: string;
  medications: string;
  allergies: string;
  blood_type: string;
  status: "active" | "inactive" | "maintenance" | "lost";
  battery_level: number;
  last_heartbeat: string | null;
  firmware_version: string;
  last_known_latitude: number | null;
  last_known_longitude: number | null;
  last_location_update: string | null;
  audio_monitoring_enabled: boolean;
  heart_rate_monitoring_enabled: boolean;
  fire_monitoring_enabled: boolean;
  fall_detection_enabled: boolean;
  monitoring_interval: number;
  registered_at: string;
  is_online: boolean;
}

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

export default function DevicesPage() {
  const [user, setUser] = useState<any | null>(null);
  const [devices, setDevices] = useState<Device[]>([]);
  const [triggers, setTriggers] = useState<EmergencyTrigger[]>([]);
  const [filteredDevices, setFilteredDevices] = useState<Device[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [deviceTypeFilter, setDeviceTypeFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [isRegisterDeviceOpen, setIsRegisterDeviceOpen] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [isDeviceDetailsOpen, setIsDeviceDetailsOpen] = useState(false);
  const [newDevice, setNewDevice] = useState({
    owner_name: "",
    owner_phone: "",
    owner_address: "",
    emergency_contact: "",
    emergency_contact_phone: "",
    medical_conditions: "",
    medications: "",
    allergies: "",
    blood_type: "",
    device_type: "guardian_bracelet",
    audio_monitoring_enabled: true,
    heart_rate_monitoring_enabled: true,
    fire_monitoring_enabled: true,
    fall_detection_enabled: true,
    monitoring_interval: 300,
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

    // Only system administrators can access devices page
    if (currentUser.role !== "System Administrator") {
      router.push("/dashboard");
      return;
    }

    fetchDevices();
    fetchEmergencyTriggers();
  }, [router]);

  useEffect(() => {
    let filtered = devices;

    if (searchTerm) {
      filtered = filtered.filter(
        (device) =>
          device.owner_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          device.serial_number
            .toLowerCase()
            .includes(searchTerm.toLowerCase()) ||
          device.owner_phone.includes(searchTerm) ||
          device.owner_address.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter((device) => device.status === statusFilter);
    }

    if (deviceTypeFilter !== "all") {
      filtered = filtered.filter(
        (device) => device.device_type === deviceTypeFilter
      );
    }

    setFilteredDevices(filtered);
  }, [devices, searchTerm, statusFilter, deviceTypeFilter]);

  const fetchDevices = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/devices/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setDevices(data.results || data);
      } else if (response.status === 401) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error fetching devices:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmergencyTriggers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/devices/triggers/",
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

  const handleRegisterDevice = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        "https://my-guardian-plus.onrender.com/api/devices/register/",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newDevice),
        }
      );

      if (response.ok) {
        fetchDevices();
        setIsRegisterDeviceOpen(false);
        setNewDevice({
          owner_name: "",
          owner_phone: "",
          owner_address: "",
          emergency_contact: "",
          emergency_contact_phone: "",
          medical_conditions: "",
          medications: "",
          allergies: "",
          blood_type: "",
          device_type: "guardian_bracelet",
          audio_monitoring_enabled: true,
          heart_rate_monitoring_enabled: true,
          fire_monitoring_enabled: true,
          fall_detection_enabled: true,
          monitoring_interval: 300,
        });
      }
    } catch (error) {
      console.error("Error registering device:", error);
    }
  };

  const acknowledgeEmergencyTrigger = async (triggerId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `https://my-guardian-plus.onrender.com/api/devices/triggers/${triggerId}/acknowledge/`,
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

  if (!user || loading) return <div>Loading...</div>;

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "default";
      case "inactive":
        return "secondary";
      case "maintenance":
        return "outline";
      case "lost":
        return "destructive";
      default:
        return "secondary";
    }
  };

  const getDeviceTypeDisplay = (type: string) => {
    switch (type) {
      case "guardian_bracelet":
        return "Guardian Bracelet";
      case "guardian_watch":
        return "Guardian Watch";
      case "guardian_pendant":
        return "Guardian Pendant";
      case "guardian_ring":
        return "Guardian Ring";
      default:
        return type;
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

  const getBatteryColor = (level: number) => {
    if (level > 50) return "text-green-600";
    if (level > 20) return "text-yellow-600";
    return "text-red-600";
  };

  const unacknowledgedTriggers = triggers.filter((t) => !t.acknowledged);

  return (
    <AuthWrapper>
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Device Management</h1>
              <p className="text-muted-foreground">
                Manage Guardian devices and monitor emergency situations
              </p>
            </div>
            {/* <Dialog
              open={isRegisterDeviceOpen}
              onOpenChange={setIsRegisterDeviceOpen}
            >
              <DialogTrigger asChild>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Register Device
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>Register New Guardian Device</DialogTitle>
                  <DialogDescription>
                    Register a new Guardian device for emergency monitoring
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="owner_name">Owner Name</Label>
                      <Input
                        id="owner_name"
                        value={newDevice.owner_name}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            owner_name: e.target.value,
                          }))
                        }
                        placeholder="Full name of device owner"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="owner_phone">Owner Phone</Label>
                      <Input
                        id="owner_phone"
                        value={newDevice.owner_phone}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            owner_phone: e.target.value,
                          }))
                        }
                        placeholder="+265991234567"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="owner_address">Owner Address</Label>
                    <Textarea
                      id="owner_address"
                      value={newDevice.owner_address}
                      onChange={(e) =>
                        setNewDevice((prev) => ({
                          ...prev,
                          owner_address: e.target.value,
                        }))
                      }
                      placeholder="Full home address"
                      rows={2}
                    />
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="emergency_contact">
                        Emergency Contact
                      </Label>
                      <Input
                        id="emergency_contact"
                        value={newDevice.emergency_contact}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            emergency_contact: e.target.value,
                          }))
                        }
                        placeholder="Emergency contact name"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="emergency_contact_phone">
                        Emergency Contact Phone
                      </Label>
                      <Input
                        id="emergency_contact_phone"
                        value={newDevice.emergency_contact_phone}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            emergency_contact_phone: e.target.value,
                          }))
                        }
                        placeholder="+265991234567"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="device_type">Device Type</Label>
                    <Select
                      value={newDevice.device_type}
                      onValueChange={(value) =>
                        setNewDevice((prev) => ({
                          ...prev,
                          device_type: value,
                        }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select device type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="guardian_bracelet">
                          Guardian Bracelet
                        </SelectItem>
                        <SelectItem value="guardian_watch">
                          Guardian Watch
                        </SelectItem>
                        <SelectItem value="guardian_pendant">
                          Guardian Pendant
                        </SelectItem>
                        <SelectItem value="guardian_ring">
                          Guardian Ring
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="blood_type">Blood Type</Label>
                      <Input
                        id="blood_type"
                        value={newDevice.blood_type}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            blood_type: e.target.value,
                          }))
                        }
                        placeholder="A+, B-, O+, etc."
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="monitoring_interval">
                        Monitoring Interval (seconds)
                      </Label>
                      <Input
                        id="monitoring_interval"
                        type="number"
                        value={newDevice.monitoring_interval}
                        onChange={(e) =>
                          setNewDevice((prev) => ({
                            ...prev,
                            monitoring_interval: Number.parseInt(
                              e.target.value
                            ),
                          }))
                        }
                        placeholder="300"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="medical_conditions">
                      Medical Conditions
                    </Label>
                    <Textarea
                      id="medical_conditions"
                      value={newDevice.medical_conditions}
                      onChange={(e) =>
                        setNewDevice((prev) => ({
                          ...prev,
                          medical_conditions: e.target.value,
                        }))
                      }
                      placeholder="Known medical conditions"
                      rows={2}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="medications">Current Medications</Label>
                    <Textarea
                      id="medications"
                      value={newDevice.medications}
                      onChange={(e) =>
                        setNewDevice((prev) => ({
                          ...prev,
                          medications: e.target.value,
                        }))
                      }
                      placeholder="Current medications"
                      rows={2}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="allergies">Allergies</Label>
                    <Textarea
                      id="allergies"
                      value={newDevice.allergies}
                      onChange={(e) =>
                        setNewDevice((prev) => ({
                          ...prev,
                          allergies: e.target.value,
                        }))
                      }
                      placeholder="Known allergies"
                      rows={2}
                    />
                  </div>

                  <div className="space-y-4">
                    <Label>Monitoring Settings</Label>
                    <div className="grid gap-4 md:grid-cols-2">
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="audio_monitoring"
                          checked={newDevice.audio_monitoring_enabled}
                          onCheckedChange={(checked) =>
                            setNewDevice((prev) => ({
                              ...prev,
                              audio_monitoring_enabled: checked,
                            }))
                          }
                        />
                        <Label htmlFor="audio_monitoring">
                          Audio Monitoring
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="heart_rate_monitoring"
                          checked={newDevice.heart_rate_monitoring_enabled}
                          onCheckedChange={(checked) =>
                            setNewDevice((prev) => ({
                              ...prev,
                              heart_rate_monitoring_enabled: checked,
                            }))
                          }
                        />
                        <Label htmlFor="heart_rate_monitoring">
                          Heart Rate Monitoring
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="fire_monitoring"
                          checked={newDevice.fire_monitoring_enabled}
                          onCheckedChange={(checked) =>
                            setNewDevice((prev) => ({
                              ...prev,
                              fire_monitoring_enabled: checked,
                            }))
                          }
                        />
                        <Label htmlFor="fire_monitoring">Fire Detection</Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="fall_detection"
                          checked={newDevice.fall_detection_enabled}
                          onCheckedChange={(checked) =>
                            setNewDevice((prev) => ({
                              ...prev,
                              fall_detection_enabled: checked,
                            }))
                          }
                        />
                        <Label htmlFor="fall_detection">Fall Detection</Label>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-2 pt-4">
                    <Button onClick={handleRegisterDevice} className="flex-1">
                      <Smartphone className="h-4 w-4 mr-2" />
                      Register Device
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => setIsRegisterDeviceOpen(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog> */}
          </div>

          {/* Emergency Triggers Alert */}
          {/*unacknowledgedTriggers.length > 0 && (
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
                  {unacknowledgedTriggers.slice(0, 3).map((trigger) => (
                    <div
                      key={trigger.trigger_id}
                      className="flex items-center justify-between p-3 bg-white border border-red-200 rounded"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={getSeverityColor(trigger.severity) as any}
                          >
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
                  {unacknowledgedTriggers.length > 3 && (
                    <p className="text-sm text-muted-foreground text-center">
                      +{unacknowledgedTriggers.length - 3} more triggers
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          )*/}

          {/* Statistics Cards */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Devices
                </CardTitle>
                <Smartphone className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{devices.length}</div>
                <p className="text-xs text-muted-foreground">
                  Registered devices
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Online Devices
                </CardTitle>
                <CheckCircle className="h-4 w-4 text-green-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {devices.filter((d) => d.is_online).length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Currently connected
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Alerts
                </CardTitle>
                <AlertTriangle className="h-4 w-4 text-red-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {unacknowledgedTriggers.length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Unacknowledged triggers
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Low Battery
                </CardTitle>
                <Battery className="h-4 w-4 text-yellow-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {devices.filter((d) => d.battery_level < 20).length}
                </div>
                <p className="text-xs text-muted-foreground">
                  Devices below 20%
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle>Search & Filter</CardTitle>
              <CardDescription>
                Find devices by owner, serial number, or location
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4 md:flex-row md:items-center">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search devices..."
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
                    <SelectItem value="inactive">Inactive</SelectItem>
                    <SelectItem value="maintenance">Maintenance</SelectItem>
                    <SelectItem value="lost">Lost/Stolen</SelectItem>
                  </SelectContent>
                </Select>
                <Select
                  value={deviceTypeFilter}
                  onValueChange={setDeviceTypeFilter}
                >
                  <SelectTrigger className="w-full md:w-[180px]">
                    <SelectValue placeholder="Filter by type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="guardian_bracelet">Bracelet</SelectItem>
                    <SelectItem value="guardian_watch">Watch</SelectItem>
                    <SelectItem value="guardian_pendant">Pendant</SelectItem>
                    <SelectItem value="guardian_ring">Ring</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Devices Table */}
          <Card>
            <CardHeader>
              <CardTitle>Devices ({filteredDevices.length})</CardTitle>
              <CardDescription>
                Manage registered Guardian devices
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Device</TableHead>
                      <TableHead>Owner</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Battery</TableHead>
                      <TableHead>Last Seen</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredDevices.map((device) => (
                      <TableRow key={device.device_id}>
                        <TableCell>
                          <div>
                            <div className="font-medium">
                              {device.serial_number}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              {getDeviceTypeDisplay(device.device_type)}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div>
                            <div className="font-medium">
                              {device.owner_name}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              {device.owner_phone}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Badge
                              variant={getStatusColor(device.status) as any}
                            >
                              {device.status}
                            </Badge>
                            {device.is_online ? (
                              <CheckCircle className="h-4 w-4 text-green-500" />
                            ) : (
                              <XCircle className="h-4 w-4 text-red-500" />
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Battery
                              className={`h-4 w-4 ${getBatteryColor(
                                device.battery_level
                              )}`}
                            />
                            <span
                              className={getBatteryColor(device.battery_level)}
                            >
                              {device.battery_level}%
                            </span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">
                            {device.last_heartbeat
                              ? new Date(device.last_heartbeat).toLocaleString()
                              : "Never"}
                          </div>
                        </TableCell>
                        <TableCell>
                          {device.last_known_latitude &&
                          device.last_known_longitude ? (
                            <div className="flex items-center gap-1">
                              <MapPin className="h-4 w-4 text-muted-foreground" />
                              <span className="text-sm">
                                {device?.last_known_latitude},{" "}
                                {device?.last_known_longitude}
                              </span>
                            </div>
                          ) : (
                            <span className="text-sm text-muted-foreground">
                              No location
                            </span>
                          )}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => {
                                setSelectedDevice(device);
                                setIsDeviceDetailsOpen(true);
                              }}
                            >
                              <Clock className="h-4 w-4" /> View Details
                            </Button>
                            {/* <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-red-600 hover:text-red-700"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button> */}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>

          {/* Device Details Dialog */}
          <Dialog
            open={isDeviceDetailsOpen}
            onOpenChange={setIsDeviceDetailsOpen}
          >
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Device Details</DialogTitle>
                <DialogDescription>
                  Detailed information about {selectedDevice?.serial_number}
                </DialogDescription>
              </DialogHeader>
              {selectedDevice && (
                <div className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label className="text-sm font-medium">
                        Serial Number
                      </Label>
                      <p className="text-sm">{selectedDevice.serial_number}</p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Device Type</Label>
                      <p className="text-sm">
                        {getDeviceTypeDisplay(selectedDevice.device_type)}
                      </p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Owner</Label>
                      <p className="text-sm">{selectedDevice.owner_name}</p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium">Phone</Label>
                      <p className="text-sm">{selectedDevice.owner_phone}</p>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">Address</Label>
                    <p className="text-sm">{selectedDevice.owner_address}</p>
                  </div>

                  {/* <div>
                    <Label className="text-sm font-medium">
                      Medical Conditions
                    </Label>
                    <p className="text-sm">
                      {selectedDevice.medical_conditions || "None reported"}
                    </p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">Medications</Label>
                    <p className="text-sm">
                      {selectedDevice.medications || "None reported"}
                    </p>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">Allergies</Label>
                    <p className="text-sm">
                      {selectedDevice.allergies || "None reported"}
                    </p>
                  </div> */}

                  <div className="grid gap-4 md:grid-cols-2">
                    {/* <div>
                      <Label className="text-sm font-medium">Blood Type</Label>
                      <p className="text-sm">
                        {selectedDevice.blood_type || "Not provided"}
                      </p>
                    </div> */}
                    <div>
                      <Label className="text-sm font-medium">
                        Firmware Version
                      </Label>
                      <p className="text-sm">
                        {selectedDevice.firmware_version}
                      </p>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Monitoring Settings
                    </Label>
                    <div className="grid gap-2 md:grid-cols-2 mt-2">
                      <div className="flex items-center gap-2">
                        {selectedDevice.audio_monitoring_enabled ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm">Audio Monitoring</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {selectedDevice.heart_rate_monitoring_enabled ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm">Heart Rate Monitoring</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {selectedDevice.fire_monitoring_enabled ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm">Fire Detection</span>
                      </div>
                      {/* <div className="flex items-center gap-2">
                        {selectedDevice.fall_detection_enabled ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm">Fall Detection</span>
                      </div> */}
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium">
                      Registration Date
                    </Label>
                    <p className="text-sm">
                      {new Date(selectedDevice.registered_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              )}
            </DialogContent>
          </Dialog>
        </div>
      </DashboardLayout>
    </AuthWrapper>
  );
}
