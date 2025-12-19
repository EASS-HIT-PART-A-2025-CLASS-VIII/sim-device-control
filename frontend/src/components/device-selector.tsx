import {
    LoadingSection,
    DeviceType,
    fetchDevices,
    useSpinnerChar,
    type DeviceInfo
} from "../utils/device-dependancies";

interface DeviceSelectorProps {
    deviceType: DeviceType;
    selectedDevice: DeviceInfo | null;
    devices: DeviceInfo[];
    loading: LoadingSection;
    onDeviceSelect: (device: DeviceInfo | null) => void;
    onRefresh: () => void;
    setLoading: (loading: LoadingSection) => void;
    setError: (error: string | null) => void;
    setDevices: (devices: DeviceInfo[]) => void;
}

export default function DeviceSelector({
    deviceType,
    selectedDevice,
    devices,
    loading,
    onDeviceSelect,
    onRefresh,
    setLoading,
    setError,
    setDevices,
}: DeviceSelectorProps) {
    const spinnerChar = useSpinnerChar(loading);

    return (
        <div style=
        {{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            justifyContent: "center",
            marginTop: "16px"
            }}>
            <select
                value={selectedDevice?.uuid || ""}
                onChange={(e) => {
                    const device =
                        devices.find(d => d.uuid === e.target.value) || null;
                    onDeviceSelect(device);
                }}
                disabled={loading !== LoadingSection.None || devices.length === 0}
                style={{
                    height: "32px",
                    minWidth: "200px",
                    padding: "0 6px",
                    boxSizing: "border-box",
                }}
            >
                <option value="">
                    {devices.length === 0 ? "No devices" : "Select device"}
                </option>
                {devices.map(d => (
                    <option key={d.uuid} value={d.uuid}>
                        {d.name}
                    </option>
                ))}
            </select>

            <button
                onClick={() => {
                    fetchDevices(deviceType, setLoading, setError, setDevices);
                    onRefresh();
                }}
                disabled={loading === LoadingSection.FetchingDevices}
                style={{
                    height: "36px",
                    width: "36px",
                    padding: 0,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
            </button>
        </div>
    );
}
