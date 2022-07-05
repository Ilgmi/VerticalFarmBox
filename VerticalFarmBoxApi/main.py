from fastapi import FastAPI
import paho.mqtt.client as mqtt
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

from verticalfarm.vertical_farm import VerticalFarm

app = FastAPI()

verticalFarm = VerticalFarm()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
