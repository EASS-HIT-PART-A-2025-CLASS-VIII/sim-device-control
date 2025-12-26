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
            _ => {
                println!("Unknown command for humidity Sensor: {}", command);
                return None;
            }
        }
    }
}
