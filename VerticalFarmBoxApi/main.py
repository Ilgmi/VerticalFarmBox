from fastapi import FastAPI
from pydantic import BaseModel

from verticalfarm.vertical_farm import VerticalFarm
import verticalfarm.messages as messages

app = FastAPI()

verticalFarm = VerticalFarm()


class RegisterBoxMessage(BaseModel):
    building: str
    room: str
    name: str


class RegisterSensorMessage(BaseModel):
    building: str
    room: str
    name: str
    type_id: str
    instance_id: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/boxes/")
async def get_boxes():
    return verticalFarm.get_boxes()

@app.post("/api/boxes")
async def add_box(box: RegisterBoxMessage):
    verticalFarm.on_box_register(messages.RegisterBoxMessage(box.building, box.room, box.name))

    return box


@app.post("/api/boxes/{box_name}/sensors/")
async def add_sensor(box_name: str, sensor: RegisterSensorMessage):
    verticalFarm.on_sensor_register(
        messages.RegisterSensorMessage(sensor.building, sensor.room, sensor.name, sensor.type_id, sensor.instance_id))
    return {"sdf": ""}
