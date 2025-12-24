use rand::Rng;

pub struct HumiditySensor;

impl HumiditySensor {
    pub fn operate(&mut self, command: &str) -> Option<String>{
        match command {
            "read_humidity" => {
                println!("Reading humidity...");
                let humidity = rand::rng().random_range(0.0..100.0);
                println!("humidity: {:.2} °C", humidity);
                return Some(humidity.to_string());
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
                println!("Unknown command for humidity Sensor: {}", command);
                return None;
            }
        }
    }
}
