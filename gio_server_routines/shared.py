import os
import subprocess
import json


def start_container(container):
    subprocess.run(["docker", "start", container])


def __json_file_path() -> str:
    # get the path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # construct the path of the json file
    return os.path.join(script_dir, "containers.json")


def stop_all_containers(save=True):
    output = subprocess.run(["docker", "ps", "-q"], capture_output=True)
    container_ids = output.stdout.decode().strip().split("\n")

    if (save):
        with open(__json_file_path(), "w") as f:
            json.dump(container_ids, f)

    for container_id in container_ids:
        subprocess.run(["docker", "stop", container_id])


def start_stopped_containers():
    with open(__json_file_path()) as f:
        container_ids = json.load(f)

    for container_id in container_ids:
        subprocess.run(["docker", "start", container_id])
