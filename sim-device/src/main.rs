mod drivers;

use rumqttc::QoS;
use dotenvy::dotenv;
use std::env;
use serde::Deserialize;

use crate::drivers::mqtt::{connect, read_payload};
use crate::drivers::device::{Device, DevicePayload, DeviceType};

#[derive(Debug, Deserialize)]
struct MqttCommand {
    command: String,
    parameter: String,
}

fn main() {
    println!("Simulated Device Running...");

    dotenv().ok();

    let device_type: String = env::var("DEVICE_TYPE").unwrap();
    let device_type: DeviceType = DeviceType::from_str(&device_type).unwrap();
    let mut device: Device = Device::new(device_type.new());
    let device_id: String = env::var("DEVICE_ID").unwrap();
    let broker: String = env::var("MQTT_BROKER").unwrap();
    let port: u16 = env::var("MQTT_PORT").unwrap().parse().unwrap();

    let (client, mut connection) = connect(&device_id, &broker, port);

    let topic = "sim-device-control/connections";
    let payload = format!("{{\"device_id\":\"{}\",\"device_type\":\"{}\",\"status\":\"connected\"}}", device_id, device_type.to_string());
    client
        .publish(
            topic,
            QoS::AtLeastOnce,
            false,
            payload)
            .unwrap();


    for event in connection.iter() {
        let payload = read_payload(event);
        if let Some(message) = payload {
            println!("Received message: {}", message);
            let topic = format!("sim-device-control/{}/response", device_id);
            println!("topic: {}", topic);
            let mut payload  = DevicePayload {
                device_id: device_id.to_string(),
                message: message.to_string(),
                response: None,
                timestamp: chrono::Utc::now().timestamp_millis() as u64,
            };
            if let Some(message) = serde_json::from_str::<MqttCommand>(&message).ok() {
                if let Some(response) = device.operate(&message.command, &message.parameter) {
                    payload.response = Some(response);
                } else {
                    payload.response = Some(format!("Invalid command: {}", message.command));
                }
            } else {
                payload.response = Some("Invalid message format".to_string());
            }
            client
                .publish(
                    topic,
                    QoS::AtLeastOnce,
                    false,
                    payload.to_string())
                    .unwrap();
            println!("Published message: {}", payload.to_string());
        }
    }
}
