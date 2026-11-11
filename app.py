from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Device(BaseModel):  
    name: str
    room: str
    temp: float 
    online: bool 


app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]

def list_devices(devices):
    for device in devices:
        print(device["name"], device["temp"])

    list_devices(readings)

def average_temp(devices):
    total = 0

    for device in devices:
        total += device["temp"]

    return total / len(devices)


def hottest(devices):
    hottest_device = devices[0]

    for device in devices:
        if device["temp"] > hottest_device["temp"]:
            hottest_device = device

    return hottest_device

@app.get("/devices")
async def get_devices_by_():
    return readings


@app.get("/devices/hottest_device")
async def get_devices_hottest_device():
    hottest_device = hottest(readings)
    return hottest_device

@app.get("/devices/online")
def get_online():
    online_devices = []
    for device in readings:
        if device["online"] is True:
            online_devices.append(device)
    return online_devices

@app.get("/devices/{name}")
def get_device(name: str):
    print("Task 4: Searching for device:", name)

    for device in readings:
        if device["name"] == name:
            return device

    raise HTTPException(
        status_code=404,
        detail="No device called " + name
    )

@app.get("/stats")
def get_stats():
   
    total_temp = 0

    for device in readings:
        total_temp += device["temp"]

    average_temp = total_temp / len(readings)

    return {
        "average_temperature": average_temp
    }

@app.post("/devices", status_code=201)
async def create_device(device: dict): 
    device_dict = device.model_dump() #convert the device model to a dictionary 
    readings.append(device)    
    return device

@app.get("/devices/room/{room}/devices")
async def get_devices_by_room(room: str):
    devices_in_room = [device for device in readings if device['room'] == room]
    if not devices_in_room:
        raise HTTPException(status_code=404, detail="No devices found in this room")
    return devices_in_room