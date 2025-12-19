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
        <div style={{ margin: "12px 0" }}>
            <button onClick={() => onAction()} disabled={isDisabled}>
                {isLoading ? spinnerChar : label}
            </button>
            <p>{value !== null && value !== undefined ? (renderValue ? renderValue(value) : <span>{value}</span>) : null}</p>
        </div>
    );
}
