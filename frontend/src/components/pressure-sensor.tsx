import { useState } from "react";
import {
  LoadingSection,
  DeviceType,
  useLoadingSpinner,
  fetchDevices,
  readStatus,
  readVersion,
  updateDescription,
  updateName,
  type DeviceInfo,
} from "./device-dependancies";

export default function PressureSensor() {
    const [pressure, setPressure] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    async function readPressure() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/pressure_sensor/read_pressure?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const textData = await response.text();
            const pressureNumber = parseFloat(textData);
            if (isNaN(pressureNumber)) {
                throw new Error("Invalid pressure value");
            }
            setPressure(pressureNumber);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Pressure Sensor</h2>

            <select value={selectedDevice?.uuid || ""} onChange={(e) => {
                const device = devices.find(d => d.uuid === e.target.value) || null;
                setSelectedDevice(device);
                setDescription(device?.description || "");
                setName(device?.name || "");
            }} disabled={loading !== LoadingSection.None || devices.length === 0}>
                <option value="">
                    {devices.length === 0 ? 'No devices' : 'Select device'}
                </option>
                {devices.map((d) => (
                    <option key={d.uuid} value={d.uuid}>
                        {d.name}
                    </option>
                ))}
            </select>

            <button onClick={() => {
                fetchDevices(DeviceType.PressureSensor, setLoading, setError, setDevices);
                setStatus(null);
                setVersion(null);
                setPressure(null);
            }}
                disabled={loading === LoadingSection.FetchingDevices}>
                {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
            </button>

            <div style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}>
                <span>Device Name:</span>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onBlur={() => {
                        updateName(
                            selectedDevice!.uuid,
                            name,
                            setLoading,
                            setError);
                        selectedDevice!.name = name;
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            updateName(
                                selectedDevice!.uuid,
                                name,
                                setLoading,
                                setError);
                            selectedDevice!.name = name;
                        }
                    }}
                    disabled={loading !== LoadingSection.None || !selectedDevice}
                />
                <span>Device Description:</span>
                <input
                    type="text"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    onBlur={() => {
                        updateDescription(
                            selectedDevice!.uuid,
                            description,
                            setLoading,
                            setError);
                        selectedDevice!.description = description;
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            updateDescription(
                                selectedDevice!.uuid,
                                description,
                                setLoading,
                                setError);
                            selectedDevice!.description = description;
                        }
                    }}
                    disabled={loading !== LoadingSection.None || !selectedDevice}
                />
                <span>Device uuid:</span>
                <span>{selectedDevice ? selectedDevice.uuid : ""}</span>
            </div>

            <button onClick={() => readStatus(selectedDevice?.uuid || "", setStatus as any, setLoading, setError)} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Get Status"}
            </button>

            <p>{status !== null && <span>Status: {status}</span>}</p>

            <button onClick={() => readVersion(selectedDevice?.uuid || "", setVersion as any, setLoading, setError)} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Get Version"}
            </button>

            <p>{version !== null && <span>Version: {version}</span>}</p>

            <button onClick={readPressure} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Read Pressure"}
            </button>

            <p>{pressure !== null && <span>Pressure: {pressure}°C</span>}</p>

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
