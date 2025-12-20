import {
    useState
} from "react";
import {
    LoadingSection,
    DeviceType,
    MotorDirection,
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
    const [actualDirection, setActualDirection] = useState<MotorDirection | null>(null);
    const [targetDirection, setTargetDirection] = useState<MotorDirection>(MotorDirection.Forward);
    const [actualAcceleration, setActualAcceleration] = useState<number | null>(null);
    const [targetAcceleration, setTargetAcceleration] = useState<number>(0);
    const [actualPosition, setActualPosition] = useState<number | null>(null);
    const [targetAbsolutePosition, setTargetAbsolutePosition] = useState<number>(0);
    const [targetRelativePosition, setTargetRelativePosition] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [version, setVersion] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    const getErrorMessage = (err: unknown) => err instanceof Error ? err.message : "Unknown error";

    async function readSpeed() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/stepper_motor/get_speed?device_uuid=${selectedDevice?.uuid}`
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
        } catch (err: unknown) {
            setError(getErrorMessage(err));
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
                `/devices/stepper_motor/set_speed?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function readDirection() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/stepper_motor/get_direction?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            setActualDirection(textData as MotorDirection);
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function writeDirection() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                device_uuid: selectedDevice!.uuid,
                direction: targetDirection as string,
            });
            const response = await fetch(
                `/devices/stepper_motor/set_direction?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function readAcceleration() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/stepper_motor/get_acceleration?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            const accelerationNumber = parseFloat(textData);
            if (isNaN(accelerationNumber)) {
                throw new Error("Invalid acceleration value");
            }
            setActualAcceleration(accelerationNumber);
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function writeAcceleration() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                device_uuid: selectedDevice!.uuid,
                acceleration: targetAcceleration.toString() ?? "0",
            });
            const response = await fetch(
                `/devices/stepper_motor/set_acceleration?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function readPosition() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const response = await fetch(
                `/devices/stepper_motor/get_location?device_uuid=${selectedDevice?.uuid}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const textData = await response.text();
            const positionNumber = parseFloat(textData);
            if (isNaN(positionNumber)) {
                throw new Error("Invalid position value");
            }
            setActualPosition(positionNumber);
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function writeAbsolutePosition() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                device_uuid: selectedDevice!.uuid,
                absolute_location: targetAbsolutePosition.toString() ?? "0",
            });
            const response = await fetch(
                `/devices/stepper_motor/set_absolute_location?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function writeRelativePosition() {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                device_uuid: selectedDevice!.uuid,
                relative_location: targetRelativePosition.toString() ?? "0",
            });
            const response = await fetch(
                `/devices/stepper_motor/set_relative_location?${params.toString()}`,
                {
                    method: 'PUT',
                }
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
        } catch (err: unknown) {
            setError(getErrorMessage(err));
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>
            <h2>Stepper Motor</h2>

            <DeviceSelector
                deviceType={DeviceType.StepperMotor}
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

            <DeviceWriteAction
                label="Set Speed"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeSpeed() : undefined}
                disabled={targetSpeed === null || !selectedDevice}
                value={targetSpeed ?? 0}
                unit="steps/second"
                onValueChange={(v) => setTargetSpeed(typeof v === 'number' ? v : parseFloat(String(v)))}
                inputType="number"
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Get Speed"
                loading={loading}
                onAction={() => selectedDevice ? readSpeed() : undefined}
                disabled={!selectedDevice}
                value={actualSpeed}
                renderValue={(v) => <span>{v} steps/second</span>}
                spinnerChar={spinnerChar}
            />

            <DeviceWriteAction
                label="Set Direction"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeDirection() : undefined}
                disabled={targetDirection === null || !selectedDevice}
                value={targetDirection ?? MotorDirection.Forward}
                onValueChange={(v) => setTargetDirection(v as MotorDirection)}
                enumOptions={Object.values(MotorDirection)}
                inputType="text"
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Get Direction"
                loading={loading}
                onAction={() => selectedDevice ? readDirection() : undefined}
                disabled={!selectedDevice}
                value={actualDirection}
                renderValue={(v) => <span>{v}</span>}
                spinnerChar={spinnerChar}
            />

            <DeviceWriteAction
                label="Set Acceleration"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeAcceleration() : undefined}
                disabled={targetAcceleration === null || !selectedDevice}
                value={targetAcceleration ?? 0}
                unit="steps/second²"
                onValueChange={(v) => setTargetAcceleration(typeof v === 'number' ? v : parseFloat(String(v)))}
                inputType="number"
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Get Acceleration"
                loading={loading}
                onAction={() => selectedDevice ? readAcceleration() : undefined}
                disabled={!selectedDevice}
                value={actualAcceleration}
                renderValue={(v) => <span>{v} steps/second²</span>}
                spinnerChar={spinnerChar}
            />

            <DeviceWriteAction
                label="Move Relative"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeRelativePosition() : undefined}
                disabled={targetRelativePosition === null || !selectedDevice}
                value={targetRelativePosition ?? 0}
                unit="steps"
                onValueChange={(v) => setTargetRelativePosition(typeof v === 'number' ? v : parseFloat(String(v)))}
                inputType="number"
                spinnerChar={spinnerChar}
            />

            <DeviceWriteAction
                label="Move Absolute"
                loading={loading}
                requiredSection={LoadingSection.UsingDevice}
                onWrite={() => selectedDevice ? writeAbsolutePosition() : undefined}
                disabled={targetAbsolutePosition === null || !selectedDevice}
                value={targetAbsolutePosition ?? 0}
                unit="steps"
                onValueChange={(v) => setTargetAbsolutePosition(typeof v === 'number' ? v : parseFloat(String(v)))}
                inputType="number"
                spinnerChar={spinnerChar}
            />

            <DeviceReadAction
                label="Get Position"
                loading={loading}
                onAction={() => selectedDevice ? readPosition() : undefined}
                disabled={!selectedDevice}
                value={actualPosition}
                renderValue={(v) => <span>{v} steps</span>}
                spinnerChar={spinnerChar}
            />

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
