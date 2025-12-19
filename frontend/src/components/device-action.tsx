import {
    LoadingSection
} from "../lib/device-dependancies";

interface DeviceActionProps {
    label: string;
    loading: LoadingSection;
    requiredSection?: LoadingSection;
    disabled?: boolean;
    onAction: () => Promise<void> | void;
    value: string | number | null;
    renderValue?: (value: string | number) => React.ReactNode;
    spinnerChar: string;
}

export default function DeviceAction({
    label,
    loading,
    requiredSection = LoadingSection.UsingDevice,
    disabled,
    onAction,
    value,
    renderValue,
    spinnerChar,
}: DeviceActionProps) {
    const isLoading = loading === requiredSection;
    const isDisabled = isLoading || disabled;

    return (
        <div style={{
            margin: "16px 0",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            minWidth: "500px",
        }}>
            <button onClick={() => onAction()} disabled={isDisabled} style={{ width: "250px" }}>
                {isLoading ? spinnerChar : label}
            </button>
            <div
                style={{
                    width: "200px",
                    minHeight: "1.5em",
                    padding: "4px 6px",
                    border: "1px solid #ccc",
                }}
            >
                {value !== null && value !== undefined
                    ? renderValue
                        ? renderValue(value)
                        : value
                    : ""}
            </div>
        </div>
    );
}
