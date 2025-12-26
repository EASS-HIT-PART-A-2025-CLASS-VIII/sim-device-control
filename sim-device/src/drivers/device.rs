use crate::drivers::temperature_sensor::TemperatureSensor;
use crate::drivers::pressure_sensor::PressureSensor;
use crate::drivers::humidity_sensor::HumiditySensor;
use crate::drivers::dc_motor::DcMotor;
use crate::drivers::stepper_motor::StepperMotor;

use std::fs::File;
use std::io::BufReader;
use serde::Deserialize;
use serde_json::Value;
use std::fs;

#[derive(Clone)]
pub enum DeviceType {
    TemperatureSensor,
    PressureSensor,
    HumiditySensor,
    DcMotor,
    StepperMotor
}

#[derive(Deserialize, Debug)]
struct DeviceInfo {
    pub name: String,
    pub description: String,
}

pub struct Device {
    pub device_type: DeviceType,
    pub temperature_sensor: Option<TemperatureSensor>,
    pub pressure_sensor: Option<PressureSensor>,
    pub humidity_sensor: Option<HumiditySensor>,
    pub dc_motor: Option<DcMotor>,
    pub stepper_motor: Option<StepperMotor>,
    pub name: String,
    pub description: String,
}

pub struct DevicePayload {
    pub id: String,
    pub device_id: String,
    pub response: Option<String>,
    pub timestamp: u64,
}

impl DevicePayload {
    pub fn to_string(&self) -> String {
        if let Some(response) = &self.response {
            return format!(
                "{{\"id\":\"{}\",\"device_id\":\"{}\",\"response\":\"{}\",\"timestamp\":{}}}",
                self.id, self.device_id, response, self.timestamp
            );
        } else {
            return format!(
                "{{\"id\":\"{}\",\"device_id\":\"{}\",\"response\":\"none\",\"timestamp\":{}}}",
                self.id, self.device_id, self.timestamp
            );
        }
    }
}

impl DeviceType {
    pub fn new(&self) -> DeviceType {
        match self {
            DeviceType::TemperatureSensor => DeviceType::TemperatureSensor,
            DeviceType::PressureSensor => DeviceType::PressureSensor,
            DeviceType::HumiditySensor => DeviceType::HumiditySensor,
            DeviceType::DcMotor => DeviceType::DcMotor,
            DeviceType::StepperMotor => DeviceType::StepperMotor,
        }
    }

    pub fn to_string(&self) -> String {
        match self {
            DeviceType::TemperatureSensor => "temperature_sensor".to_string(),
            DeviceType::PressureSensor => "pressure_sensor".to_string(),
            DeviceType::HumiditySensor => "humidity_sensor".to_string(),
            DeviceType::DcMotor => "dc_motor".to_string(),
            DeviceType::StepperMotor => "stepper_motor".to_string(),
        }
    }
    
    pub fn from_str(device_type: &str) -> Option<DeviceType> {
        match device_type {
            "temperature_sensor" => Some(DeviceType::TemperatureSensor),
            "pressure_sensor" => Some(DeviceType::PressureSensor),
            "humidity_sensor" => Some(DeviceType::HumiditySensor),
            "dc_motor" => Some(DeviceType::DcMotor),
            "stepper_motor" => Some(DeviceType::StepperMotor),
            _ => None,
        }
    }
}

impl Device {
    pub fn new(device_type: DeviceType) -> Device {
        let file = File::open("device_info.json").expect("Cannot open file");
        let reader = BufReader::new(file);

        let device_info: DeviceInfo = serde_json::from_reader(reader).expect("Error parsing JSON");

        match device_type {
            DeviceType::TemperatureSensor => Device {
                device_type,
                temperature_sensor: Some(TemperatureSensor),
                pressure_sensor: None,
                humidity_sensor: None,
                dc_motor: None,
                stepper_motor: None,
                name: device_info.name,
                description: device_info.description,
            },
            DeviceType::PressureSensor => Device {
                device_type,
                temperature_sensor: None,
                pressure_sensor: Some(PressureSensor),
                humidity_sensor: None,
                dc_motor: None,
                stepper_motor: None,
                name: device_info.name,
                description: device_info.description,
            },
            DeviceType::HumiditySensor => Device {
                device_type,
                temperature_sensor: None,
                pressure_sensor: None,
                humidity_sensor: Some(HumiditySensor),
                dc_motor: None,
                stepper_motor: None,
                name: device_info.name,
                description: device_info.description,
            },
            DeviceType::DcMotor => Device {
                device_type,
                temperature_sensor: None,
                pressure_sensor: None,
                humidity_sensor: None,
                dc_motor: Some(DcMotor::new()),
                stepper_motor: None,
                name: device_info.name,
                description: device_info.description,
            },
            DeviceType::StepperMotor => Device {
                device_type,
                temperature_sensor: None,
                pressure_sensor: None,
                humidity_sensor: None,
                dc_motor: None,
                stepper_motor: Some(StepperMotor::new()),
                name: device_info.name,
                description: device_info.description,
            },
        }
    }

    pub fn operate(&mut self, command: &str, parameter: &str) -> Option<String> {
        match command {
            "get_status" => {
                println!("Getting status...");
                return Some("Rust Simulation".to_string());
            }
            "get_version" => {
                println!("Getting version...");
                return Some("1.0.0".to_string());
            }
            "set_name" => {
                println!("Setting name to {}", parameter);
                self.name = parameter.to_string();
                let data = fs::read_to_string("device_info.json").expect("Unable to read file");
                let mut json: Value = serde_json::from_str(&data).expect("JSON was not well-formatted");
                json["name"] = Value::String(parameter.to_string());
                fs::write
                    ("device_info.json",
                    serde_json::to_string_pretty(&json)
                        .unwrap()
                    ).expect("Unable to write file");
                return Some(parameter.to_string());
            }
            "set_description" => {
                println!("Setting description to {}", parameter);
                self.description = parameter.to_string();
                let data = fs::read_to_string("device_info.json").expect("Unable to read file");
                let mut json: Value = serde_json::from_str(&data).expect("JSON was not well-formatted");
                json["description"] = Value::String(parameter.to_string());
                fs::write
                    ("device_info.json",
                    serde_json::to_string_pretty(&json)
                        .unwrap()
                    ).expect("Unable to write file");
                return Some(parameter.to_string());
            }
            _ => {}
        }
        match self.device_type {
            DeviceType::TemperatureSensor => {
                if let Some(device) = &mut self.temperature_sensor {
                    return device.operate(command);
                }
                return None;
            }
            DeviceType::PressureSensor => {
                if let Some(device) = &mut self.pressure_sensor {
                    return device.operate(command);
                }
                return None;
            }
            DeviceType::HumiditySensor => {
                if let Some(device) = &mut self.humidity_sensor {
                    return device.operate(command);
                }
                return None;
            }
            DeviceType::DcMotor => {
                if let Some(device) = &mut self.dc_motor {
                    return device.operate(command, parameter);
                }
                return None;
            }
            DeviceType::StepperMotor => {
                if let Some(device) = &mut self.stepper_motor {
                    return device.operate(command, parameter);
                }
                return None;
            }
        }
    }
}