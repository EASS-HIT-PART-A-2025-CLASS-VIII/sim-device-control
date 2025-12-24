pub struct DcMotor {
    speed: f64,
    direction: bool, // true = forward, false = backward
}

impl DcMotor {
    pub fn new() -> Self {
        DcMotor {
            speed: 0.0,
            direction: true,
        }
    }

    pub fn operate(&mut self, command: &str, parameter: &str) -> Option<String>{
        match command {
            "get_speed" => {
                println!("Reading speed...");
                println!("speed: {:.2} %", self.speed);
                return Some(self.speed.to_string());
            }
            "set_speed" => {
                println!("Setting speed to {} %...", parameter);
                if let Ok(set_speed) = parameter.parse::<f64>() {
                    if set_speed >= 0.0 && set_speed <= 100.0 {
                        self.speed = set_speed;
                        println!("Speed set to {:.2} %", self.speed);
                        return Some(self.speed.to_string());
                    } else {
                        println!("Invalid speed value: {}", parameter);
                        return None;
                    }
                } else {
                    println!("Invalid speed parameter: {}", parameter);
                    return None;
                }
            }
            "get_direction" => {
                println!("Reading direction...");
                println!("direction: {}", if self.direction { "forward" } else { "backward" });
                return Some(self.direction.to_string());
            }
            "set_direction" => {
                println!("Setting direction to {} %...", parameter);
                if let Ok(set_direction) = parameter.parse::<bool>() {
                    self.direction = set_direction;
                    println!("Direction set to {}", if self.direction { "forward" } else { "backward" });
                    return Some(self.direction.to_string());
                } else {
                    println!("Invalid direction parameter: {}", parameter);
                    return None;
                }
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
                println!("Unknown command for DC motor: {}", command);
                return None;
            }
        }
    }
}
