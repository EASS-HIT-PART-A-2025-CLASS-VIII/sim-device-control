use rumqttc::{Client, Event, Incoming, MqttOptions, QoS};
use std::time::Duration;

pub fn connect(device_id: &str, broker: &str, port: u16) -> (rumqttc::Client, rumqttc::Connection) {

    let mut mqtt_options = MqttOptions::new(device_id, broker, port);
    mqtt_options.set_keep_alive(Duration::from_secs(10));

    let (client, connection) = Client::new(mqtt_options, 10);
    
    let topic = format!("sim-device-control/{}/command", device_id);

    client.subscribe(&topic, QoS::AtLeastOnce).unwrap();

    println!("Listening for messages on topic: {}", topic);

    return (client, connection);
}

pub fn read_payload(event: Result<rumqttc::Event, rumqttc::ConnectionError>) -> Option<String> {
    if let Ok(Event::Incoming(Incoming::Publish(message))) = event {
        let payload = String::from_utf8_lossy(&message.payload);
        let payload: String = String::from(payload.trim());
        return Some(payload);
    } else {
        return None;
    }
}
