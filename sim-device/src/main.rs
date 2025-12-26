mod drivers;

use rumqttc::QoS;
use dotenvy::dotenv;
use std::env;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
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

    // Setup signal handler for graceful shutdown
    let running = Arc::new(AtomicBool::new(true));
    let r = running.clone();
    let client_shutdown = client.clone();
    let device_id_shutdown = device_id.clone();
    let device_type_shutdown = device_type.clone();
    
    ctrlc::set_handler(move || {
        println!("\nShutdown signal received, disconnecting...");
        send_disconnect_notification(&client_shutdown, &device_id_shutdown, &device_type_shutdown);
        r.store(false, Ordering::SeqCst);
    }).expect("Error setting Ctrl-C handler");

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
        if !running.load(Ordering::SeqCst) {
            break;
        }
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
    
    // Normal exit - send disconnect notification if not already sent
    if running.load(Ordering::SeqCst) {
        println!("Application closing, disconnecting...");
        send_disconnect_notification(&client, &device_id, &device_type);
    }
    
    println!("Shutdown complete.");
}

fn send_disconnect_notification(client: &rumqttc::Client, device_id: &str, device_type: &DeviceType) {
    let topic = "sim-device-control/connections";
    let payload = format!(
        "{{\"device_id\":\"{}\",\"device_type\":\"{}\",\"status\":\"disconnected\"}}",
        device_id,
        device_type.to_string()
    );
    
    match client.publish(topic, QoS::AtLeastOnce, false, payload) {
        Ok(_) => {
            println!("Disconnect notification sent successfully");
            // Give time for the message to be sent
            std::thread::sleep(std::time::Duration::from_millis(500));
        }
        Err(e) => {
            eprintln!("Failed to send disconnect notification: {}", e);
        }
    }
}
