#!/usr/bin/env python3
from os.path import expanduser
import os

from sh import mosquitto_pub, tail

LOG_FILE = os.environ.get("LOG_FILE", "~/Library/Application Support/Objective-See/OverSight/OverSight.log")
MQTT_BROKER = os.environ['MQTT_BROKER']
MQTT_TOPICS = os.environ['MQTT_TOPICS']

def send_message(on_air):
    groups = zip(*[iter(MQTT_TOPICS.split(":"))] * 3)
    for topic, on_payload, off_payload in groups:
        payload = on_payload if on_air else off_payload
        mosquitto_pub("-h", MQTT_BROKER, "-t", topic, "-m", payload)

def main():
    for line in tail("-n", 0, "-f", expanduser(LOG_FILE), _iter=True):
        if line.find("Video Device became active") > -1:
            print("Camera is active")
            send_message(True)
        elif line.find("Video Device became inactive") > -1:
            print("Camera is inactive")
            send_message(False)


if __name__ == "__main__":
    main()
