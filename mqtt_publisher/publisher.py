import time
import random
import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "solar/plant1/data"

client = mqtt.Client()
client.connect(broker, port, 60)

while True:
    solar_data = {
        "voltage": round(random.uniform(200, 240), 2),
        "current": round(random.uniform(5, 15), 2),
        "power": round(random.uniform(1000, 3000), 2)
    }
    client.publish(topic, str(solar_data))
    print(f"Published: {solar_data}")
    time.sleep(5)
