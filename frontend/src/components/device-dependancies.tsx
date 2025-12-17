import { useEffect, useState } from "react";

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
}

export interface DeviceInfo {
    uuid: string;
    name: string;
    status: string;
    description: string;
    type: DeviceType;
}

const spinnerChars = ['|', '/', '—', '\\'];

export function useLoadingSpinner(initial: LoadingSection = LoadingSection.None) {
    const [loading, setLoading] = useState<LoadingSection>(initial);
    const [spinnerIndex, setSpinnerIndex] = useState(0);

    useEffect(() => {
        let id: number | undefined;
        if (loading !== LoadingSection.None) {
            id = window.setInterval(() => {
                setSpinnerIndex((i) => (i + 1) % spinnerChars.length);
            }, 120);
        } else {
            setSpinnerIndex(0);
        }
        return () => {
            if (id !== undefined) clearInterval(id);
        };
    }, [loading]);

    const spinnerChar = spinnerChars[spinnerIndex];

    return { loading, setLoading, spinnerChar } as const;
}

export async function fetchDevices
    (deviceType: DeviceType,
        setLoading: (loading: LoadingSection) => void,
        setError: (error: string | null) => void,
        setDevices: (devices: Array<DeviceInfo>) => void) {
    setLoading(LoadingSection.FetchingDevices);
    setError(null);
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const response = await fetch('/devices/type/' + deviceType);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
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
            });
        }
        setDevices(mapped);
    } catch (err: any) {
        setError(err.message || "Unknown error");
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
            `/devices/get_status?device_uuid=${deviceUuid}`
        );
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const textData = await response.text();
        setStatus(textData);
    } catch (err: any) {
        setError(err.message || "Unknown error");
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
            `/devices/get_version?device_uuid=${deviceUuid}`
        );
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const textData = await response.text();
        setVersion(textData);
    } catch (err: any) {
        setError(err.message || "Unknown error");
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
        new_description: newDescription,
        });
        const response = await fetch(
            `/devices/update_description/${deviceUuid}?${params.toString()}`,
            {
                method: 'PUT',
            }
        );
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
    } catch (err: any) {
        setError(err.message || "Unknown error");
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
        new_name: newName,
        });
        const response = await fetch(
            `/devices/update_name/${deviceUuid}?${params.toString()}`,
            {
                method: 'PUT',
            }
        );
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
    } catch (err: any) {
        setError(err.message || "Unknown error");
    } finally {
        setLoading(LoadingSection.None);
    }
}