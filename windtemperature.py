#!/usr/bin/env python3
import serial
import time
import paho.mqtt.client as mqtt
import re

# --- Wind sensor (USB serial) ---
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

# --- Temp sensor (DS18B20) ---
# Replace with your actual device ID if different
device_file = '/sys/bus/w1/devices/28-06201884371b/w1_slave'

def read_temp():
    """Read temperature in °C from DS18B20"""
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip().endswith("YES"):
            return float(lines[1].split("t=")[-1]) / 1000.0
    except:
        return None
    return None

def parse_wind(line):
    """Extract numeric wind speed from strings like 'Vindhastighet: 2.00 m/s'"""
    match = re.search(r"([0-9]+(\.[0-9]+)?)", line.replace(",", "."))
    if match:
        return float(match.group(1))
    return None

# --- MQTT setup ---
BROKER = "100.82.0.4"
PORT = 1883
BASE_TOPIC = "pi12"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("elektronik", "elektronik")  # required for broker
client.connect(BROKER, PORT, 60)
client.loop_start()

print(f"Publishing wind + temp to mqtt://{BROKER}:{PORT} ({BASE_TOPIC}/sensor/1 and /sensor/2)")

# --- Main loop ---
try:
    while True:
        # --- Wind ---
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        wind_value = parse_wind(line) if line else None

        if wind_value is not None:
            print(f"{BASE_TOPIC}/sensor/1 = {wind_value:.2f}")
            client.publish(f"{BASE_TOPIC}/sensor/1", str(wind_value))

        # --- Temp ---
        temp_value = read_temp()
        if temp_value is not None:
            print(f"{BASE_TOPIC}/sensor/2 = {temp_value:.2f}")
            client.publish(f"{BASE_TOPIC}/sensor/2", str(temp_value))

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user.")
    client.loop_stop()
    client.disconnect()
    ser.close()
