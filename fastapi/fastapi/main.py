from fastapi import FastAPI, HTTPException, Query
from enum import Enum
import subprocess
import json

class ContainerNameEnum(str, Enum):
    ping = "ping"
    speedtest = "speedtest"
    iperf = "iperf"

app = FastAPI()

@app.post("/send_json_string")
async def send_json_string(container_name: ContainerNameEnum, json_data: dict):
    try:
        # Convert the JSON string to a dictionary
        data = json_data

        # Additional logic for specific containers
        if container_name == ContainerNameEnum.iperf or container_name == ContainerNameEnum.ping:
            # Write data to the shared volume
            with open("/app/data/data.json", "w") as file:
                json.dump(data, file)

        # Run the Docker command to start the selected container
        subprocess.run(["docker", "start", container_name.value])

        return {"message": f"JSON string written to shared volume. Container {container_name} started successfully."}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON string")
