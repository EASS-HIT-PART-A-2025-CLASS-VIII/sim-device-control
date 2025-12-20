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

export default function HumiditySensor() {
    const [humidity, setHumidity] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    async function readHumidity() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/humidity_sensor/read_humidity?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            const humidityNumber = parseFloat(textData);
            if (isNaN(humidityNumber)) {
                throw new Error("Invalid humidity value");
            }
            setHumidity(humidityNumber);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Unknown error";
            setError(message);
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Humidity Sensor</h2>

            <DeviceSelector
                deviceType={DeviceType.HumiditySensor}
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
                    setHumidity(null);
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
                    (s) => setStatus(s),
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
                    (v) => setVersion(v),
                    setLoading,
                    setError
                ) : undefined}
                disabled={!selectedDevice}
                value={version}
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Read Humidity"
                loading={loading}
                onAction={() => selectedDevice ? readHumidity() : undefined}
                disabled={!selectedDevice}
                value={humidity}
                renderValue={(v) => <span>{v}%</span>}
                spinnerChar={spinnerChar}
            />

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
