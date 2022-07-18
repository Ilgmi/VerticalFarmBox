from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import verticalfarm.messages as messages
from verticalfarm.vertical_farm import VerticalFarm


origins = [
    "http://localhost",
    "http://localhost:4200",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verticalFarm = VerticalFarm()
verticalFarm.listen_to_box_connections()

print(datetime.now().strftime("%d-%m-%YT%H:%M:%S"))

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
    sensor_type: str

class MoveRoof(BaseModel):
    directoin: bool
    steps: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/boxes/")
async def get_boxes(skip: int = 0, limit: int = 10):
    b = verticalFarm.get_boxes(skip, limit)
    return b


@app.get("/api/buildings/{building}/rooms/{room}/boxes/{box}")
async def get_box(building, room, box):
    return verticalFarm.get_box(building + "/" + room + "/" + box)


@app.post("/api/boxes")
async def add_box(box: RegisterBoxMessage):
    verticalFarm.on_box_register(messages.RegisterBoxMessage(box.building, box.room, box.name))

    return box

@app.get("/api/buildings/{building}/rooms/{room}/boxes/{box}/sensors-data")
async def get_sensors_data(building, room, box):
    return verticalFarm.get_box_sensors_data(building + "/" + room + "/" + box)

@app.post("/api/buildings/{building}/rooms/{room}/boxes/{box}/toggle-roof")
async def get_sensors_data(building, room, box):
    return verticalFarm.toggle_roof(building + "/" + room + "/" + box)

@app.post("/api/buildings/{building}/rooms/{room}/boxes/{box}/water-plant")
async def get_sensors_data(building, room, box):
    return verticalFarm.water_plant(building + "/" + room + "/" + box)

@app.post("/api/buildings/{building}/rooms/{room}/boxes/{box}/move-roof")
async def get_sensors_data(building, room, box, move_roof: MoveRoof):
    return verticalFarm.move_roof(building + "/" + room + "/" + box, move_roof)


@app.get("/api/boxes/{box_name}/sensors")
async def get_sernsors_from_boxes(box_name: str):
    return verticalFarm.get_sensors(box_name)


@app.post("/api/boxes/{box_name}/sensors/")
async def add_sensor(box_name: str, sensor: RegisterSensorMessage):
    verticalFarm.on_sensor_register(
        messages.RegisterSensorMessage(sensor.building, sensor.room, sensor.name, sensor.type_id, sensor.instance_id,
                                       sensor.sensor_type))
    return {"sdf": ""}
