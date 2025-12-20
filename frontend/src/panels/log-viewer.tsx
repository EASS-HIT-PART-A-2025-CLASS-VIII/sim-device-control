import {
    useState
} from "react";
import {
    LoadingSection,
    useLoadingSpinner,
    type LogEntry,
} from "../utils/device-dependancies";

export default function LogViewer() {
    const [error, setError] = useState<string | null>(null);
    const [logEntries, setLogEntries] = useState<Array<LogEntry>>([]);
    const [start_time, setStartTime] = useState<string>("");
    const [end_time, setEndTime] = useState<string>("");
    const { loading, setLoading, spinnerChar } = useLoadingSpinner();

    const [newLogEntry, setNewLogEntry] = useState<LogEntry>({
        uuid: "",
        user: "",
        device_uuid: "",
        action: "",
        description: "",
        timestamp: "",
    });

    async function createLogEntry(
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void,
    ) {
        setLoading(LoadingSection.UsingDevice);
        setError(null);
        try {
            const params = new URLSearchParams({
                action: newLogEntry.action,
                description: newLogEntry.description,
            });
            const response = await fetch(
                `/logs/?${params.toString()}`,
                {
                    method: "POST",
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

    async function fetchLogEntries(
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void,
        setLogEntries: (entries: Array<LogEntry>) => void,
    ) {
        setLoading(LoadingSection.FetchingDevices);
        setError(null);
        try {
            const response = await fetch(
                `/logs/`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const data = await response.json();
            setLogEntries(data);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    async function fetchFilteredLogEntries(
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void,
        setLogEntries: (entries: Array<LogEntry>) => void,
    ) {
        setLoading(LoadingSection.FetchingDevices);
        setError(null);
        try {
            const params = new URLSearchParams({
                start_time: start_time.replace('T', 'T').slice(0, 19),
                end_time: end_time.replace('T', 'T').slice(0, 19),
            });
            const response = await fetch(
                `/logs/filtered?${params.toString()}`
            );
            if (!response.ok) {
                const body = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
            }
            const data = await response.json();
            setLogEntries(data);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(LoadingSection.None);
        }
    }

    return (
        <div>

            <h2>Create Log Entry</h2>

            <div style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}>
                <span>action:</span>
                <input
                    type="text"
                    value={newLogEntry.action}
                    onChange={(e) => setNewLogEntry({ ...newLogEntry, action: e.target.value })}
                    disabled={loading !== LoadingSection.None}
                />
                <span>description:</span>
                <input
                    type="text"
                    value={newLogEntry.description}
                    onChange={(e) => setNewLogEntry({ ...newLogEntry, description: e.target.value })}
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
                    await createLogEntry(setLoading, setError);
                }}
                    disabled={
                        loading === LoadingSection.UsingDevice
                        || !newLogEntry.action.trim() || !newLogEntry.description.trim()
                    }
                    style={{ width: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {loading === LoadingSection.UsingDevice ? spinnerChar : "+"}
                </button>
            </div>

            <h2>Log Entries</h2>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    marginTop: "16px",
                }}>
                <button onClick={() => {
                    start_time === "" && end_time === "" ? fetchLogEntries(setLoading, setError, setLogEntries) : fetchFilteredLogEntries(setLoading, setError, setLogEntries);
                }}
                    disabled={loading === LoadingSection.FetchingDevices}
                    style={{ width: "40px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {loading === LoadingSection.FetchingDevices ? spinnerChar : "⟳"}
                </button>
            </div>

            <div style={{
                textAlign: "left",
                display: "grid",
                gridTemplateColumns: "150px auto",
                gap: "8px 16px",
                marginTop: "16px",
            }}>
                <span>start time:</span>
                <input
                    type="datetime-local"
                    value={start_time}
                    onChange={(e) => setStartTime(e.target.value)}
                    disabled={loading !== LoadingSection.None}
                />
                <span>end time:</span>
                <input
                    type="datetime-local"
                    value={end_time}
                    onChange={(e) => setEndTime(e.target.value)}
                    disabled={loading !== LoadingSection.None}
                />
            </div>

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
                            }}>user</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                            }}>device uuid</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                            }}>description</th>
                            <th style={{
                                textAlign: 'center',
                                borderBottom: '2px solid #e6e6e6',
                                padding: '8px'
                            }}>timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logEntries.map((option) => (
                            <tr
                                key={option.uuid}
                                style={{
                                    cursor: 'pointer',
                                    transition: 'background 0.15s'
                                }}
                            >
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                }}>{option.uuid}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                }}>{option.user}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                }}>{option.device_uuid}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                }}>{option.description}</td>
                                <td style={{
                                    borderBottom: '1px solid #f0f0f0', padding: '8px',
                                }}>{option.timestamp}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

            </div>

            <p>{error && <div style={{ color: "red" }}>Error: {error}</div>}</p>
        </div>
    );
}
