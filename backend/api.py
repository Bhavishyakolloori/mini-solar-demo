from fastapi import FastAPI
from influxdb_client import InfluxDBClient

app = FastAPI()

token = "OTTtqNf-R1abz0yW4pdQaTEyDhJEdxvoL_-Tiox79-ZTPF9qBBy7HIjtk-DYt4dzXfFHztRBdXxwd6-RAwU7xw=="
org = "Solar"
bucket = "Solar-DB"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

@app.get("/solar-data")
def get_solar_data():
    flux_query = f'from(bucket:"{bucket}") |> range(start: -5m) |> last()'
    try:
        tables = query_api.query(flux_query, org=org)
        data = {}
        for table in tables:
            for record in table.records:
                field = record.get_field()      # get the field name, e.g., voltage/current/power
                value = record.get_value()      # get the field value
                data[field] = value
        if not data:
            return {"status": "ok", "message": "No recent data found"}
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
