import { useState } from "react";
import {
  LoadingSection,
  DeviceType,
  useLoadingSpinner,
  fetchDevices,
  readStatus,
  readVersion,
} from "./device-dependancies";

export default function HumiditySensor() {
    const [humidity, setHumidity] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<string>("");
    const [devices, setDevices] = useState<Array<{ uuid: string; name: string; status: string; description: string }>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    async function readHumidity() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/humidity_sensor/read_humidity?device_uuid=${selectedDevice}`
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const textData = await response.text();
            const humidityNumber = parseFloat(textData);
            if (isNaN(humidityNumber)) {
                throw new Error("Invalid humidity value");
            }
            setHumidity(humidityNumber);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Humidity Sensor</h2>

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
                fetchDevices(DeviceType.HumiditySensor, setLoading, setError, setDevices);
                setStatus(null);
                setVersion(null);
                setHumidity(null);
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

            <button onClick={readHumidity} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "Read Humidity"}
            </button>

            <br />
            <br />

            {humidity !== null && <span>Humidity: {humidity} Pa</span>}
            {error && <div style={{ color: "red" }}>Error: {error}</div>}
        </div>
    );
}
