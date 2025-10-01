import serial
import time
import json
import paho.mqtt.client as mqtt

# --- Wind sensor (USB serial) ---
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

# --- Temp sensor (DS18B20 with your ID) ---
device_file = '/sys/bus/w1/devices/28-06201884371b/w1_slave'

def read_temp():
    """Read temperature in °C from DS18B20"""
    with open(device_file, 'r') as f:
        lines = f.readlines()
    if lines[0].strip()[-3:] != 'YES':
        return None
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0
    return None

# --- MQTT setup ---
BROKER = "100.82.0.4"   # or IP of your broker
PORT = 1883
TOPIC = "Pi2"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)

print("Reading wind + temperature... publishing to MQTT and console")

while True:
    try:
        # --- Wind ---
        wind_line = ser.readline().decode('utf-8', errors='ignore').strip()
        wind_value = None
        if wind_line:
            try:
                wind_value = float(wind_line)
            except ValueError:
                print("Raw wind data (not numeric):", wind_line)

        # --- Temp ---
        temp_value = read_temp()

        # --- Print and publish both ---
        if wind_value is not None and temp_value is not None:
            print(f"🌬️ Wind: {wind_value:.2f} m/s | 🌡️ Temp: {temp_value:.2f} °C")
            payload = json.dumps({"wind": wind_value, "temp": temp_value})
            client.publish(TOPIC, payload)
        elif wind_value is not None:
            print(f"🌬️ Wind: {wind_value:.2f} m/s | 🌡️ Temp: --")
            payload = json.dumps({"wind": wind_value})
            client.publish(TOPIC, payload)
        elif temp_value is not None:
            print(f"🌬️ Wind: -- | 🌡️ Temp: {temp_value:.2f} °C")
            payload = json.dumps({"temp": temp_value})
            client.publish(TOPIC, payload)

        time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break

