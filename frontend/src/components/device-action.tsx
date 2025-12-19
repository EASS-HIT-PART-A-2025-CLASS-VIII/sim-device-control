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
        <div
            style={{
                margin: "16px 0",
                display: "flex",
                flexDirection: "column",
                gap: "8px",
                maxWidth: "320px",
            }}
        >
            <button
                onClick={onAction}
                disabled={isDisabled}
                style={{
                    padding: "8px 14px",
                    borderRadius: "6px",
                    border: "1px solid #ccc",
                    backgroundColor: isDisabled ? "#f5f5f5" : "#007bff",
                    color: isDisabled ? "#999" : "#fff",
                    cursor: isDisabled ? "not-allowed" : "pointer",
                    fontSize: "14px",
                    fontWeight: 500,
                    transition: "background-color 0.2s ease",
                }}
            >
                {isLoading ? spinnerChar : label}
            </button>

            {value !== null && value !== undefined && (
                <div
                    style={{
                        padding: "6px 10px",
                        borderRadius: "4px",
                        backgroundColor: "#f9f9f9",
                        border: "1px solid #eee",
                        fontSize: "13px",
                        color: "#333",
                    }}
                >
                    {renderValue ? renderValue(value) : <span>{value}</span>}
                </div>
            )}
        </div>
    );
}
