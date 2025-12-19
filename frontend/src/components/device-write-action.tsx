import type { ReactNode } from "react";
import { LoadingSection } from "../utils/device-dependancies";

interface DeviceWriteActionProps {
    label: string;
    loading: LoadingSection;
    requiredSection?: LoadingSection;
    disabled?: boolean;
    onWrite: (value: string | number) => Promise<void> | void;
    value: string | number | null;
    unit?: string | null;
    onValueChange: (value: string | number) => void;
    renderControl?: (value: string | number | null, onChange: (value: string | number) => void, disabled: boolean) => ReactNode;
    inputType?: 'text' | 'number';
    options?: Array<{ label: string; value: string | number }>;
    enumOptions?: Array<string | number>;
    spinnerChar: string;
}

export default function DeviceWriteAction({
    label,
    loading,
    requiredSection = LoadingSection.UsingDevice,
    disabled,
    onWrite,
    value,
    unit,
    onValueChange,
    renderControl,
    inputType = 'text',
    options,
    enumOptions,
    spinnerChar,
}: DeviceWriteActionProps) {
    const isLoading = loading === requiredSection;
    const isDisabled = isLoading || !!disabled;

    return (
        <div style={{
            margin: "16px 0",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            minWidth: "500px",
        }}>
            <button
                onClick={() => onWrite(value ?? (inputType === 'number' ? 0 : ''))}
                disabled={isDisabled || value === ""}
                style={{ width: "250px" }}
            >
                {isLoading ? spinnerChar : label}
            </button>
            {renderControl ? (
                renderControl(value, onValueChange, isDisabled)
            ) : (options && options.length > 0) || (enumOptions && enumOptions.length > 0) ? (
                <select
                    value={value !== null && value !== undefined ? String(value) : ''}
                    onChange={(e) => {
                        const raw = e.target.value;
                        const next = inputType === 'number' ? Number(raw) : raw;
                        onValueChange(next);
                    }}
                    disabled={isDisabled}
                    style={{
                        width: "200px",
                        minHeight: "1.5em",
                        padding: "4px 6px",
                        border: "1px solid #ccc",
                    }}
                >
                    {options?.map((opt) => (
                        <option key={String(opt.value)} value={String(opt.value)}>
                            {opt.label}
                        </option>
                    ))}
                    {enumOptions?.map((opt) => (
                        <option key={String(opt)} value={String(opt)}>
                            {String(opt)}
                        </option>
                    ))}
                </select>
            ) : (
                <input
                    type={inputType}
                    value={value !== null && value !== undefined ? String(value) : ''}
                    onChange={(e) => {
                        const raw = e.target.value;
                        const next = inputType === 'number' ? Number(raw) : raw;
                        onValueChange(next);
                    }}
                    disabled={isDisabled}
                    style={{
                        width: "200px",
                        minHeight: "1.5em",
                        padding: "4px 6px",
                        border: "1px solid #ccc",
                    }}
                />
            )}
            {unit ? (
                <span style={{ minWidth: "40px", textAlign: "left" }}>{unit}</span>
            ) : null}
        </div>
    );
}
