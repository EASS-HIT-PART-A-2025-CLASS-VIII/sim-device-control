import {
    LoadingSection,
    DeviceType,
    fetchDevices,
    useSpinnerChar,
    type DeviceInfo
} from "../lib/device-dependancies";

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
        <>
            <select
                value={selectedDevice?.uuid || ""}
                onChange={(e) => {
                    const device = devices.find(d => d.uuid === e.target.value) || null;
                    onDeviceSelect(device);
                }}
                disabled={loading !== LoadingSection.None || devices.length === 0}
            >
                <option value="">
                    {devices.length === 0 ? 'No devices' : 'Select device'}
                </option>
                {devices.map((d) => (
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
            >
                {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
            </button>
        </>
    );
}
