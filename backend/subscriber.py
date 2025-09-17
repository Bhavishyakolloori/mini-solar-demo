import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions
import ast

# InfluxDB setup
token = "OTTtqNf-R1abz0yW4pdQaTEyDhJEdxvoL_-Tiox79-ZTPF9qBBy7HIjtk-DYt4dzXfFHztRBdXxwd6-RAwU7xw=="
org = "Solar"
bucket = "Solar-DB"
url = "http://localhost:8086"

client_influx = InfluxDBClient(url=url, token=token, org=org)
write_api = client_influx.write_api(write_options=WriteOptions(batch_size=1))

# MQTT setup
broker = "localhost"
port = 1883
topic = "solar/plant1/data"

def on_message(client, userdata, msg):
    try:
        data = ast.literal_eval(msg.payload.decode())
        print(f"Received: {data}")

        point = (
            Point("solar_metrics")
            .tag("plant", "plant1")
            .field("voltage", data["voltage"])
            .field("current", data["current"])
            .field("power", data["power"])
        )
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(f"Error: {e}")

mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
mqtt_client.on_message = on_message
mqtt_client.connect(broker, port, 60)
mqtt_client.subscribe(topic)
mqtt_client.loop_forever()
