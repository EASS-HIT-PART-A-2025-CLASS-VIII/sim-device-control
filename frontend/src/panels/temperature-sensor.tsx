import {
    useState
} from "react";
import {
  LoadingSection,
  DeviceType,
  useLoadingSpinner,
  readStatus,
  readVersion,
  type DeviceInfo,
} from "../utils/device-dependancies";
import DeviceSelector from "../components/device-selector";
import DeviceDetails from "../components/device-details";
import DeviceReadAction from "../components/device-read-action";

export default function TemperatureSensor() {
    const [temperature, setTemperature] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    const getErrorMessage = (err: unknown) => err instanceof Error ? err.message : "Unknown error";

    async function readTemperature() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/temperature_sensor/read_temperature?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            const temperatureNumber = parseFloat(textData);
            if (isNaN(temperatureNumber)) {
                throw new Error("Invalid temperature value");
            }
            setTemperature(temperatureNumber);
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Temperature Sensor</h2>

            <DeviceSelector
                deviceType={DeviceType.TemperatureSensor}
                selectedDevice={selectedDevice}
                devices={devices}
                loading={loading}
                onDeviceSelect={(device) => {
                    setSelectedDevice(device);
                    setDescription(device?.description || "");
                    setName(device?.name || "");
                }}
                onRefresh={() => {
                    setStatus(null);
                    setVersion(null);
                    setTemperature(null);
                }}
                setLoading={setLoading}
                setError={setError}
                setDevices={setDevices}
            />

            <DeviceDetails
                selectedDevice={selectedDevice}
                name={name}
                description={description}
                loading={loading}
                setName={setName}
                setDescription={setDescription}
                setLoading={setLoading}
                setError={setError}
            />

            <DeviceReadAction
                label="Get Status"
                loading={loading}
                onAction={() => selectedDevice ? readStatus(
                    selectedDevice.uuid,
                    (value) => setStatus(value),
                    setLoading,
                    setError
                ) : undefined}
                disabled={!selectedDevice}
                value={status}
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Get Version"
                loading={loading}
                onAction={() => selectedDevice ? readVersion(
                    selectedDevice.uuid,
                    (value) => setVersion(value),
                    setLoading,
                    setError
                ) : undefined}
                disabled={!selectedDevice}
                value={version}
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Read Temperature"
                loading={loading}
                onAction={() => selectedDevice ? readTemperature() : undefined}
                disabled={!selectedDevice}
                value={temperature}
                renderValue={(v) => <span>{v}°C</span>}
                spinnerChar={spinnerChar}
            />

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
