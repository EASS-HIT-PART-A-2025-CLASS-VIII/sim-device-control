import {
    useEffect,
    useState
} from "react";

export enum LoadingSection {
    None = 0,
    FetchingDevices = 1,
    UsingDevice = 2,
}

export enum DeviceType {
    None = "",
    TemperatureSensor = "temperature_sensor",
    PressureSensor = "pressure_sensor",
    HumiditySensor = "humidity_sensor",
    DcMotor = "dc_motor",
    StepperMotor = "stepper_motor",
    All = "all",
}

export interface DeviceInfo {
    uuid: string;
    type: DeviceType;
    name: string;
    description: string;
    version: string;
    status: string;
}

export interface LogEntry {
    uuid: string;
    user: string;
    device_uuid: string;
    action: string;
    description: string;
    timestamp: string;
}

export enum MotorDirection {
    Forward = "forward",
    Backward = "backward",
}

const spinnerChars = ['|', '/', '—', '\\'];
const getErrorMessage = (err: unknown) => err instanceof Error ? err.message : "Unknown error";

export function useLoadingSpinner(initial: LoadingSection = LoadingSection.None) {
    const [loading, setLoading] = useState<LoadingSection>(initial);
    const [spinnerIndex, setSpinnerIndex] = useState(0);

    useEffect(() => {
        if (loading === LoadingSection.None) {
            return;
        }

        const id = window.setInterval(() => {
            setSpinnerIndex((i) => (i + 1) % spinnerChars.length);
        }, 120);

        return () => {
            clearInterval(id);
            setSpinnerIndex(0);
        };
    }, [loading]);

    const spinnerChar = spinnerChars[spinnerIndex];

    return { loading, setLoading, spinnerChar } as const;
}

export function useSpinnerChar(loading: LoadingSection) {
    const [spinnerIndex, setSpinnerIndex] = useState(0);

    useEffect(() => {
        if (loading === LoadingSection.None) {
            return;
        }

        const id = window.setInterval(() => {
            setSpinnerIndex((i) => (i + 1) % spinnerChars.length);
        }, 120);

        return () => {
            clearInterval(id);
            setSpinnerIndex(0);
        };
    }, [loading]);

    return spinnerChars[spinnerIndex];
}

export async function fetchDevices
    (deviceType: DeviceType,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void,
        setDevices: (devices: Array<DeviceInfo>) => void) {
    setLoading(LoadingSection.FetchingDevices);
    setError(null);
    try {
        const response = deviceType === DeviceType.All ? await fetch('/devices/') : await fetch('/devices/type/' + deviceType);
        if (!response.ok) {
            const body = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
        }
        const data = await response.json();
        const mapped = Array<DeviceInfo>();
        for (const item of data) {
            mapped.push({
                uuid: item.uuid,
                name: item.name,
                status: item.status,
                description: item.description,
                type: item.type,
                version: item.version,
            });
        }
        setDevices(mapped);
    } catch (err: unknown) {
        setError(getErrorMessage(err));
    } finally {
        setLoading(LoadingSection.None);
    }
}

export async function readStatus
    (deviceUuid: string,
        setStatus: (status: string) => void,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const response = await fetch(
            `/devices/get_status?device_uuid=${deviceUuid.trim()}`
        );
        if (!response.ok) {
            const body = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
        }
        const textData = await response.text();
        setStatus(textData);
    } catch (err: unknown) {
        setError(getErrorMessage(err));
    } finally {
        setLoading(LoadingSection.None);
    }
}

export async function readVersion
    (deviceUuid: string,
        setVersion: (status: string) => void,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const response = await fetch(
            `/devices/get_version?device_uuid=${deviceUuid.trim()}`
        );
        if (!response.ok) {
            const body = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, description: ${body.detail}`);
        }
        const textData = await response.text();
        setVersion(textData);
    } catch (err: unknown) {
        setError(getErrorMessage(err));
    } finally {
        setLoading(LoadingSection.None);
    }
}

export async function updateDescription
    (deviceUuid: string,
        newDescription: string,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const params = new URLSearchParams({
            new_description: newDescription.trim(),
        });
        const response = await fetch(
            `/devices/update_description/${deviceUuid.trim()}?${params.toString()}`,
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

export async function updateName
    (deviceUuid: string,
        newName: string,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const params = new URLSearchParams({
        new_name: newName.trim(),
        });
        const response = await fetch(
            `/devices/update_name/${deviceUuid.trim()}?${params.toString()}`,
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

export async function deleteDevice
    (deviceUuid: string,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const response = await fetch(
            `/devices/${deviceUuid.trim()}`,
            {
                method: 'DELETE',
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

export async function createDevice
    (deviceInfo: DeviceInfo,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void) {
    setLoading(LoadingSection.UsingDevice);
    setError(null);
    try {
        const trimmedDeviceInfo = Object.fromEntries(
            Object.entries(deviceInfo).map(([key, value]) => [
                key,
                typeof value === "string" ? value.trim() : value,
            ])
        ) as typeof deviceInfo;

        const response = await fetch(
            `/devices/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(trimmedDeviceInfo),
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