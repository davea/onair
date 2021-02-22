#!/usr/bin/env python3
"""
Sends commands directly to the Trådfri gateway instead of via MQTT.
Requires coap-client to be installed thus and on the PATH, as demonstrated
in https://github.com/home-assistant-libs/pytradfri/blob/master/script/install-coap-client.sh
"""
from dotenv import load_dotenv
load_dotenv()

import os
import atexit

import logging
logging.basicConfig(level=logging.INFO)

from sh import coap_client, pkill, Command

TRADFRI_IP = os.environ['TRADFRI_IP']
TRADFRI_USER = os.environ['TRADFRI_USER']
TRADFRI_KEY = os.environ['TRADFRI_KEY']
TRADFRI_LIGHTS = os.environ['TRADFRI_LIGHTS']
TRADFRI_TEMPLATE = os.environ['TRADFRI_TEMPLATE']

def send_message(on_air):
    groups = zip(*[iter(TRADFRI_LIGHTS.split(":"))] * 3)
    for device, on_payload, off_payload in groups:
        payload = on_payload if on_air else off_payload
        stdin = TRADFRI_TEMPLATE % payload
        url = f"coaps://{TRADFRI_IP}:5684/15001/{device}"
        coap_client("-u", TRADFRI_USER, "-k", TRADFRI_KEY, "-v", "0", "-m", "put", "-e", stdin, url)

def main():
    kill_helper() # tidy up any stale helpers
    onair_helper = Command("./onair_helper")(_iter=True)
    try:
        for line in onair_helper:
            if line.find("Camera active") > -1:
                print("Switching on because:", line, flush=True)
                send_message(True)
            elif line.find("Camera inactive") > -1:
                print("Switching off because:", line, flush=True)
                send_message(False)
    finally:
        print("Exiting", flush=True)
        onair_helper.terminate()

@atexit.register
def kill_helper():
    print("kill_helper", flush=True)
    try:
        pkill("onair_helper")
    except Exception:
        pass

if __name__ == "__main__":
    main()
