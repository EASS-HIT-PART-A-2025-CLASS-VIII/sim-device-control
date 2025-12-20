export enum PanelType {
    None = "",
    DeviceList = "device_list",
    TemperatureSensor = "temperature_sensor",
    PressureSensor = "pressure_sensor",
    HumiditySensor = "humidity_sensor",
    DcMotor = "dc_motor",
    StepperMotor = "stepper_motor",
    Logs = "logs",
}

export interface PanelOption {
    type: PanelType;
    label: string;
    description: string;
}

export const deviceTypeOptions: PanelOption[] = [
  { type: PanelType.DeviceList,
    label: 'Device List',
    description: 'View or create devices' },
  { type: PanelType.TemperatureSensor,
    label: 'Temperature Sensor',
    description: 'Temperature sensor device' },
  { type: PanelType.PressureSensor,
    label: 'Pressure Sensor',
    description: 'Pressure sensor device' },
  { type: PanelType.HumiditySensor,
    label: 'Humidity Sensor',
    description: 'Humidity sensor device' },
  { type: PanelType.DcMotor,
    label: 'DC Motor',
    description: 'DC motor device' },
  { type: PanelType.StepperMotor,
    label: 'Stepper Motor',
    description: 'Stepper motor device' },
  { type: PanelType.Logs,
    label: 'Logs',
    description: 'View or create logs' },
]
