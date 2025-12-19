import {
    useState
} from "react";
import {
    LoadingSection,
    DeviceType,
    useLoadingSpinner,
    fetchDevices,
    deleteDevice,
    createDevice,
    updateDescription,
    updateName,
    type DeviceInfo,
} from "../utils/device-dependancies";

export default function TemperatureSensor() {
    const [error, setError] = useState<string | null>(null);
    const [selectedDevice, setSelectedDevice] = useState<DeviceInfo | null>(null);
    const [description, setDescription] = useState(selectedDevice?.description ?? "");
    const [name, setName] = useState(selectedDevice?.name ?? "");
    const [devices, setDevices] = useState<Array<DeviceInfo>>([]);
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    const [newDevice, setNewDevice] = useState<DeviceInfo>({
        uuid: "",
        type: DeviceType.TemperatureSensor,
        name: "",
        description: "",
        version: "",
        status: "",
    });

    return (
        <div>

            <h2>Create Device</h2>

            <div style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}>
                <span>uuid:</span>
                <input
                    type="text"
                    value={newDevice.uuid}
                    onChange={(e) => setNewDevice({ ...newDevice, uuid: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
                <span>type:</span>
                <select
                    value={newDevice.type}
                    onChange={(e) => setNewDevice({ ...newDevice, type: e.target.value as DeviceType })}
                    disabled={loading !== LoadingSection.None}
                >
                    {Object.entries(DeviceType)
                        .filter(([_, value]) => value !== DeviceType.All && value !== DeviceType.None)
                        .map(([_, value]) => (
                            <option key={value} value={value}>
                                {value}
                            </option>
                        ))}
                </select>
                <span>name:</span>
                <input
                    type="text"
                    value={newDevice.name}
                    onChange={(e) => setNewDevice({ ...newDevice, name: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
                <span>description:</span>
                <input
                    type="text"
                    value={newDevice.description}
                    onChange={(e) => setNewDevice({ ...newDevice, description: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
                <span>version:</span>
                <input
                    type="text"
                    value={newDevice.version}
                    onChange={(e) => setNewDevice({ ...newDevice, version: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
                <span>status:</span>
                <input
                    type="text"
                    value={newDevice.status}
                    onChange={(e) => setNewDevice({ ...newDevice, status: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
            </div>
            
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    marginTop: "16px",
                }}>
                <button onClick={async () => {
                    await createDevice(newDevice, setLoading, setError);
                    fetchDevices(DeviceType.All, setLoading, setError, setDevices);
                }}
                    disabled={
                        loading === LoadingSection.UsingDevice
                        || !newDevice.uuid.trim() || !newDevice.name.trim() || !newDevice.description.trim()
                        || !newDevice.version.trim() || !newDevice.status.trim()
                    }
                    style={{ width: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {loading === LoadingSection.UsingDevice ? spinnerChar : "+"}
                </button>
            </div>

            <h2>Device List</h2>

            <div>

                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>uuid</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>type</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>name</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>description</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>version</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                                }}>status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {devices.map((option) => (
                            <tr
                                key={option.uuid}
                                onClick={() => {
                                    setSelectedDevice(selectedDevice === option ? null : option);
                                    setDescription(selectedDevice === option ? "" : option.description);
                                    setName(selectedDevice === option ? "" : option.name);
                                }}
                                style={{
                                    cursor: 'pointer',
                                    background: selectedDevice === option ? '#f5f7ff' : 'transparent',
                                    transition: 'background 0.15s'
                                }}
                            >
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.uuid}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.type}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.name}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.description}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.version}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                    color: selectedDevice === option ? '#000' : '#e6e6e6'
                                    }}>{option.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

            </div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    marginTop: "16px",
                }}>

            <button onClick={() => {
                fetchDevices(DeviceType.All, setLoading, setError, setDevices);
            }}
                disabled={loading === LoadingSection.FetchingDevices}
                style={{ width: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
            </button>

            <button onClick={async () => {
                await deleteDevice(selectedDevice!.uuid, setLoading, setError);
                fetchDevices(DeviceType.All, setLoading, setError, setDevices);
                setSelectedDevice(null);
                setDescription("");
                setName("");
            }} disabled={loading === LoadingSection.UsingDevice || !selectedDevice}
            style={{ width: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {loading === LoadingSection.UsingDevice ? spinnerChar : "—"}
            </button>

            </div>
            <div style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}>
                <span>Device Name:</span>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onBlur={() => {
                        updateName(
                            selectedDevice!.uuid,
                            name,
                            setLoading,
                            setError);
                        selectedDevice!.name = name;
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            updateName(
                                selectedDevice!.uuid,
                                name,
                                setLoading,
                                setError);
                            selectedDevice!.name = name;
                        }
                    }}
                    disabled={loading !== LoadingSection.None || !selectedDevice}
                />
                <span>Device Description:</span>
                <input
                    type="text"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    onBlur={() => {
                        updateDescription(
                            selectedDevice!.uuid,
                            description,
                            setLoading,
                            setError);
                        selectedDevice!.description = description;
                    }}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            updateDescription(
                                selectedDevice!.uuid,
                                description,
                                setLoading,
                                setError);
                            selectedDevice!.description = description;
                        }
                    }}
                    disabled={loading !== LoadingSection.None || !selectedDevice}
                />
            </div>

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
