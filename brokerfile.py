import paho.mqtt.client as mqtt

BROKER = "100.82.0.4"   # din broker
PORT = 1883
TOPIC = "Pi2"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

client.loop_start()

result = client.publish(TOPIC, "Meddelande från Pi 🚀")
result.wait_for_publish()

print(f"📤 Skickat till {BROKER} topic {TOPIC}")

client.loop_stop()
client.disconnect()
