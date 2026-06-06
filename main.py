from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()


class Traffic(BaseModel):
    id: int
    location: str
    vehicle_count: int
    congestion_level: str


# Here we get all the traffic records

@app.get("/traffic")
def get_all_traffic():

    with open("traffic.json", "r") as file:
        data = json.load(file)

    return data


# We get single record by id
@app.get("/traffic/{traffic_id}")
def get_traffic(traffic_id: int):

    with open("traffic.json", "r") as file:
        data = json.load(file)

    for traffic in data:

        if traffic["id"] == traffic_id:
            return traffic

    return {"message": "Traffic record not found"}


# We can add records by using POST method
@app.post("/traffic")
def add_traffic(record: Traffic):

    with open("traffic.json", "r") as file:
        data = json.load(file)

    data.append(record.model_dump())

    with open("traffic.json", "w") as file:
        json.dump(data, file, indent=4)

    return {"message": "Traffic record added"}


# Update record by using PUT method
@app.put("/traffic/{traffic_id}")
def update_traffic(
    traffic_id: int,
    updated_record: Traffic
):

    with open("traffic.json", "r") as file:
        data = json.load(file)

    for traffic in data:

        if traffic["id"] == traffic_id:

            traffic["location"] = updated_record.location
            traffic["vehicle_count"] = updated_record.vehicle_count
            traffic["congestion_level"] = updated_record.congestion_level

            with open("traffic.json", "w") as file:
                json.dump(data, file, indent=4)

            return {"message": "Traffic record updated"}

    return {"message": "Traffic record not found"}


# Delete records
@app.delete("/traffic/{traffic_id}")
def delete_traffic(traffic_id: int):

    with open("traffic.json", "r") as file:
        data = json.load(file)

    for traffic in data:

        if traffic["id"] == traffic_id:

            data.remove(traffic)

            with open("traffic.json", "w") as file:
                json.dump(data, file, indent=4)

            return {"message": "Traffic record deleted"}

    return {"message": "Traffic record not found"}