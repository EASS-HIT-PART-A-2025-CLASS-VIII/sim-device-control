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
            _ => {
                println!("Unknown command for pressure Sensor: {}", command);
                return None;
            }
        }
    }
}
