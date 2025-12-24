use rand::Rng;

pub struct TemperatureSensor;

impl TemperatureSensor {
    pub fn operate(&mut self, command: &str) -> Option<String> {
            match command {
                "read_temperature" => {
                    println!("Reading temperature...");
                let temperature = rand::rng().random_range(0.0..100.0);
                println!("Temperature: {:.2} °C", temperature);
                return Some(temperature.to_string());
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
                println!("Unknown command for Temperature Sensor: {}", command);
                return None;
            }
        }
    }
}