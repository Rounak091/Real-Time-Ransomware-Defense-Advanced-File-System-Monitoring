import time
import json
import paho.mqtt.client as mqtt

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    
    devices = ["smart_camera", "temperature_sensor", "door_lock"]
    
    for i in range(100):
        for device in devices:
            msg = {
                "device": device,
                "event": "heartbeat",
                "timestamp": time.time(),
                "value": i
            }
            client.publish(f"home/devices/{device}", json.dumps(msg))
            time.sleep(0.5)
    
    client.disconnect()

if __name__ == "__main__":
    main()