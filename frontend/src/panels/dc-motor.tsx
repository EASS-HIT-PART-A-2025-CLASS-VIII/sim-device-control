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
import DeviceWriteAction from "../components/device-write-action";

export default function DcMotor() {
    const [actualSpeed, setActualSpeed] = useState<number | null>(null);
    const [targetSpeed, setTargetSpeed] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    async function readSpeed() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/dc_motor/get_speed?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            const speedNumber = parseFloat(textData);
            if (isNaN(speedNumber)) {
                throw new Error("Invalid speed value");
            }
            setActualSpeed(speedNumber);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function writeSpeed() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                device_uuid: selectedDevice!.uuid,
                speed: targetSpeed.toString() ?? "0",
            });
            const response = await fetch(
                `/devices/dc_motor/set_speed?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Humidity Sensor</h2>

            <DeviceSelector
                deviceType={DeviceType.DcMotor}
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
                    setActualSpeed(null);
                    setTargetSpeed(0);
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

            <DeviceWriteAction
                label="Set Speed"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeSpeed() : undefined}
                disabled={targetSpeed === null || !selectedDevice}
                value={targetSpeed ?? 0}
                onValueChange={(v) => setTargetSpeed(typeof v === 'number' ? v : parseFloat(String(v)))}
                inputType="number"
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="get Speed"
                loading={loading}
                onAction={() => selectedDevice ? readSpeed() : undefined}
                disabled={!selectedDevice}
                value={actualSpeed}
                renderValue={(v) => <span>Speed: {v} %</span>}
                spinnerChar={spinnerChar}
            />

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
