"use client";

import {
  MapContainer,
  TileLayer,
  Marker,
  useMapEvents,
  LayersControl,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";

const { BaseLayer } = LayersControl;

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

const DEFAULT_POSITION = [-13.9833, 33.7833]; // Lilongwe

export default function MapSelector({
  latitude,
  longitude,
  onSelect,
}: {
  latitude: number;
  longitude: number;
  onSelect: (lat: number, lng: number) => void;
}) {
  const [position, setPosition] = useState(
    latitude && longitude ? [latitude, longitude] : DEFAULT_POSITION
  );

  function LocationMarker() {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng;
        // Round coordinates to fit backend constraints:
        // Latitude: max_digits=10, decimal_places=8 (XX.XXXXXXXX)
        // Longitude: max_digits=11, decimal_places=8 (XXX.XXXXXXXX)
        const roundedLat = Math.round(lat * 100000000) / 100000000; // 8 decimal places
        const roundedLng = Math.round(lng * 100000000) / 100000000; // 8 decimal places

        setPosition([roundedLat, roundedLng]);
        onSelect(roundedLat, roundedLng);
      },
    });

    return <Marker position={position} />;
  }

  return (
    <MapContainer
      center={position}
      zoom={13}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%", borderRadius: "0.5rem" }}
    >
      <LayersControl position="topright">
        <BaseLayer checked name="Standard View">
          <TileLayer
            attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
        </BaseLayer>

        <BaseLayer name="Satellite View">
          <TileLayer
            attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye"
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          />
        </BaseLayer>
      </LayersControl>

      <LocationMarker />
    </MapContainer>
  );
}
