from fastapi import FastAPI, HTTPException, Query
from enum import Enum
import subprocess
import json

class ContainerNameEnum(str, Enum):
    ping = "ping"
    speedtest = "speedtest"
    iperf_avg = "iperf_avg"
    iperf = "iperf"

app = FastAPI()

@app.post("/launch_container")
async def send_json_string(container_name: ContainerNameEnum, json_data: dict):
    try:
        # Convert the JSON string to a dictionary
        data = json_data

        # Additional logic for specific containers
        if container_name == ContainerNameEnum.iperf or container_name == ContainerNameEnum.ping or container_name == ContainerNameEnum.iperf_avg:
            # Write data to the shared volume
            with open("/app/data/data.json", "w") as file:
                json.dump(data, file)

        # Run the Docker command to start the selected container
        subprocess.run(["docker", "start", container_name.value])

        return {"message": f"JSON string written to shared volume. Container {container_name} started successfully."}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON string")

@app.post("/stop_container")
async def send_json_string(container_name: ContainerNameEnum):
    try:
        
        # Run the Docker command to start the selected container
        subprocess.run(["docker", "stop", container_name.value])

        return {"message": f"JSON string written to shared volume. Container {container_name} started successfully."}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON string")
