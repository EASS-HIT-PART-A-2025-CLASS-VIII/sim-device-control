pub struct StepperMotor {
    speed: f64,
    acceleration: f64,
    direction: bool, // true = forward, false = backward
    location: f64,
}

impl StepperMotor {
    pub fn new() -> Self {
        StepperMotor {
            speed: 0.0,
            acceleration: 0.0,
            direction: true,
            location: 0.0,
        }
    }

    pub fn operate(&mut self, command: &str, parameter: &str) -> Option<String>{
        match command {
            "get_speed" => {
                println!("Reading speed...");
                println!("speed: {:.2} steps/second", self.speed);
                return Some(self.speed.to_string());
            }
            "set_speed" => {
                println!("Setting speed to {} %...", parameter);
                if let Ok(set_speed) = parameter.parse::<f64>() {
                    if set_speed >= 0.0 && set_speed <= 100.0 {
                        self.speed = set_speed;
                        println!("Speed set to {:.2} steps/second", self.speed);
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
            "get_acceleration" => {
                println!("Reading acceleration...");
                println!("acceleration: {:.2} %", self.acceleration);
                return Some(self.acceleration.to_string());
            }
            "set_acceleration" => {
                println!("Setting acceleration to {} %...", parameter);
                if let Ok(set_acceleration) = parameter.parse::<f64>() {
                    self.acceleration = set_acceleration;
                    println!("Acceleration set to {:.2} steps/second²", self.acceleration);
                    return Some(self.acceleration.to_string());
                } else {
                    println!("Invalid acceleration parameter: {}", parameter);
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
            "get_location" => {
                println!("Reading location...");
                println!("location: {:.2} steps", self.location);
                return Some(self.location.to_string());
            }
            "set_location_relative" => {
                println!("Setting relative location to +/-{} steps...", parameter);
                if let Ok(set_location) = parameter.parse::<f64>() {
                    self.location += set_location;
                    println!("Location set to {:.2} steps", self.location);
                    return Some(self.location.to_string());
                } else {
                    println!("Invalid location parameter: {}", parameter);
                    return None;
                }
            }
            "set_location_absolute" => {
                println!("Setting absolute location to {} steps...", parameter);
                if let Ok(set_location) = parameter.parse::<f64>() {
                    self.location = set_location;
                    println!("Location set to {:.2} steps", self.location);
                    return Some(self.location.to_string());
                } else {
                    println!("Invalid location parameter: {}", parameter);
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
