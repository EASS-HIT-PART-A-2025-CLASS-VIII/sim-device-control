use rand::Rng;

pub struct PressureSensor;

impl PressureSensor {
    pub fn operate(&mut self, command: &str) -> Option<String>{
        match command {
            "read_pressure" => {
                println!("Reading pressure...");
                let pressure = rand::rng().random_range(0.0..100.0);
                println!("pressure: {:.2} °C", pressure);
                return Some(pressure.to_string());
            }
            "get_status" => {
                println!("Getting status...");
                let status = "Rust Simulation";
                println!("Status: {}", status);
                return Some(status.to_string());
            }
            "get_version" => {
                println!("Getting version...");
                let version = "1.0.0";
                println!("Version: {}", version);
                return Some(version.to_string());
            }
            _ => {
                println!("Unknown command for pressure Sensor: {}", command);
                return None;
            }
        }
    }
}
