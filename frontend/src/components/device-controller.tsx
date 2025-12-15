import { useEffect, useState } from "react";

enum LoadingSection {
  None = 0,
  FetchingDevices = 1,
  UsingDevice = 2,
}

export default function TemperatureSensor() {
  const [temperature, setTemperature] = useState<number | null>(null);
  const [loading, setLoading] = useState<LoadingSection>(LoadingSection.None);
  const [error, setError] = useState<string | null>(null);
  const [selectedDevice, setSelectedDevice] = useState<string>("");
  const [devices, setDevices] = useState<Array<{ uuid: string; name: string; status: string; description: string }>>([]);
  const [spinnerIndex, setSpinnerIndex] = useState(0);
  const spinnerChars = ['|', '/', '—', '\\'];

  useEffect(() => {
    let id: number | undefined;
    if (loading !== LoadingSection.None) {
      id = window.setInterval(() => {
        setSpinnerIndex((i) => (i + 1) % spinnerChars.length);
      }, 120);
    } else {
      setSpinnerIndex(0);
    }
    return () => {
      if (id !== undefined) clearInterval(id);
    };
  }, [loading]);

  const spinnerChar = spinnerChars[spinnerIndex];

  async function readTemperature() {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
      const response = await fetch(
        `/devices/temperature_sensor/read_temperature?device_uuid=${selectedDevice}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const textData = await response.text();
      const temperatureNumber = parseFloat(textData);
      if (isNaN(temperatureNumber)) {
        throw new Error("Invalid temperature value");
      }
      setTemperature(temperatureNumber);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(LoadingSection.None);
    }
  }

  async function fetchDevices() {
    setLoading(LoadingSection.FetchingDevices);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      const response = await fetch('/devices/type/temperature_sensor');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      // Ensure we have an array and pick only relevant fields
      const mapped = Array.isArray(data)
        ? data.map((d: any) => ({
            uuid: d.uuid,
            name: d.name,
            status: d.status,
            description: d.description,
          }))
        : [];
      setDevices(mapped);
      // If nothing selected yet, default to the first device
      if (!selectedDevice && mapped.length > 0) {
        setSelectedDevice(mapped[0].uuid);
      }
    } catch (err: any) {
        setError(err.message || "Unknown error");
    } finally {
        setLoading(LoadingSection.None);
    }
  }

  return (
    <div>
      <h2>Temperature Sensor Component</h2>

      <select value={selectedDevice} onChange={(e) => setSelectedDevice(e.target.value)} disabled={loading !== LoadingSection.None || devices.length === 0}>
        <option value="">{devices.length === 0 ? 'No devices' : 'Select device'}</option>
        {devices.map((d) => (
          <option key={d.uuid} value={d.uuid}>
            {d.name} {d.status ? `(${d.status})` : ''}
          </option>
        ))}
      </select>

      <button onClick={fetchDevices} disabled={loading === LoadingSection.FetchingDevices}>
        {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
      </button>

      <br />
      <br />

      <button onClick={readTemperature} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}>
        {loading === LoadingSection.UsingDevice ? spinnerChar : "Read Temperature"}
      </button>

      <br />
      <br />

      {temperature !== null && <span>Temperature: {temperature}°C</span>}
      {error && <div style={{ color: "red" }}>Error: {error}</div>}
    </div>
  );
}
