import {
    LoadingSection,
    type DeviceInfo,
    updateDescription,
    updateName
} from "../utils/device-dependancies";

interface DeviceDetailsProps {
    selectedDevice: DeviceInfo | null;
    name: string;
    description: string;
    loading: LoadingSection;
    setName: (value: string) => void;
    setDescription: (value: string) => void;
    setLoading: (loading: LoadingSection) => void;
    setError: (error: string | null) => void;
}

export default function DeviceDetails({
    selectedDevice,
    name,
    description,
    loading,
    setName,
    setDescription,
    setLoading,
    setError,
}: DeviceDetailsProps) {
    const disabled = loading !== LoadingSection.None || !selectedDevice;

    const persistName = () => {
        if (!selectedDevice) return;
        updateName(selectedDevice.uuid, name, setLoading, setError);
    };

    const persistDescription = () => {
        if (!selectedDevice) return;
        updateDescription(selectedDevice.uuid, description, setLoading, setError);
    };

    return (
        <div
            style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}
        >
            <span>Device Name:</span>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onBlur={persistName}
                onKeyDown={(e) => {
                    if (e.key === "Enter") persistName();
                }}
                disabled={disabled}
            />
            <span>Device Description:</span>
            <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                onBlur={persistDescription}
                onKeyDown={(e) => {
                    if (e.key === "Enter") persistDescription();
                }}
                disabled={disabled}
            />
            <span>Device uuid:</span>
            <span>{selectedDevice ? selectedDevice.uuid : ""}</span>
        </div>
    );
}
