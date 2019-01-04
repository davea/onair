#!/usr/bin/env python3
import os

from sh import mosquitto_pub, Command

MQTT_BROKER = os.environ['MQTT_BROKER']
MQTT_TOPICS = os.environ['MQTT_TOPICS']

def send_message(on_air):
    groups = zip(*[iter(MQTT_TOPICS.split(":"))] * 3)
    for topic, on_payload, off_payload in groups:
        payload = on_payload if on_air else off_payload
        mosquitto_pub("-h", MQTT_BROKER, "-t", topic, "-m", payload)

def main():
    onair_helper = Command("./onair_helper")(_iter=True)
    try:
        for line in onair_helper:
            if line.find("Camera active") > -1:
                print("Switching on because:", line)
                send_message(True)
            elif line.find("Camera inactive") > -1:
                print("Switching off because:", line)
                send_message(False)
    finally:
        onair_helper.terminate()


if __name__ == "__main__":
    main()
