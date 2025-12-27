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
                if self.direction {
                    return Some("forward".to_string());
                } else {
                    return Some("backward".to_string());
                }
            }
            "set_direction" => {
                println!("Setting direction to {} %...", parameter);
                let set_direction = parameter.parse::<String>().unwrap_or_default();
                if set_direction.to_lowercase() == "forward" {
                    self.direction = true;
                } else if set_direction.to_lowercase() == "backward" {
                    self.direction = false;
                } else {
                    println!("Invalid direction value: {}", parameter);
                    return None;
                }
                println!("Direction set to {}", if self.direction { "forward" } else { "backward" });
                if self.direction {
                    return Some("forward".to_string());
                } else {
                    return Some("backward".to_string());
                }
            }
            _ => {
                println!("Unknown command for DC motor: {}", command);
                return None;
            }
        }
    }
}
