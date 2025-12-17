import { useState } from "react";
import {
  LoadingSection,
  DeviceType,
  useLoadingSpinner,
  fetchDevices,
  readStatus,
  readVersion,
} from "./device-dependancies";

export default function PressureSensor() {
    const [pressure, setPressure] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<string>("");
    const [devices, setDevices] = useState<Array<{ uuid: string; name: string; status: string; description: string }>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    async function readPressure() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/pressure_sensor/read_pressure?device_uuid=${selectedDevice}`
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

            <select value={selectedDevice} onChange={(e) => setSelectedDevice(e.target.value)} disabled={loading !== LoadingSection.None || devices.length === 0}>
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

            <br />
            <br />

            <button onClick={() => readStatus(selectedDevice, setStatus as any, setLoading, setError)} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Get Status"}
            </button>

            <br />
            <br />

            {status !== null && <span>Status: {status}</span>}

            <br />
            <br />

            <button onClick={() => readVersion(selectedDevice, setVersion as any, setLoading, setError)} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Get Version"}
            </button>

            <br />
            <br />

            {version !== null && <span>Version: {version}</span>}

            <br />
            <br />

            <button onClick={readPressure} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Read Pressure"}
            </button>

            <br />
            <br />

            {pressure !== null && <span>Pressure: {pressure} Pa</span>}
            {error && <div style={{ color: "red" }}>Error: {error}</div>}
        </div>
    );
}
