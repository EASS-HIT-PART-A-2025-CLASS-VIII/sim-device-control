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
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
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

            <DeviceSelector
                deviceType={DeviceType.PressureSensor}
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
                    setPressure(null);
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
                    setStatus as any,
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
                    setVersion as any,
                    setLoading,
                    setError
                ) : undefined}
                disabled={!selectedDevice}
                value={version}
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Read Pressure"
                loading={loading}
                onAction={() => selectedDevice ? readPressure() : undefined}
                disabled={!selectedDevice}
                value={pressure}
                renderValue={(v) => <span>Pressure: {v} hPa</span>}
                spinnerChar={spinnerChar}
            />

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
