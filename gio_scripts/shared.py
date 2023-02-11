import os
import subprocess
import json
import concurrent.futures

root_folder = '/mnt/c/Users/vhviv/APPS/docker-hk4e'
mysql_folder = root_folder + '/data/mysql'
redis_folder = root_folder + '/data/redis'
logs_folder = root_folder + '/logs'
log_file = os.path.dirname(os.path.abspath(__file__)) + '/scripts_logs.log'

# Those should not be killed
gio_containers_ids = ["5ba91c23b08c", "9d798e153d02", "365577a49ae6", "4afa6a7964ff",
                      "7532be99d3ed", "0e3f5838538b", "59d264589438", "cfd9bc6d3dac"]


def get_local_json_file_path(file_name: str) -> str:
    """Takes a file name as an argument and returns the path of the json file. It does this by getting the path of the current script and joining it with the file name."""
    # get the path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # construct the path of the json file
    return os.path.join(script_dir, file_name)


def stop_container(container_id):
    """Takes a container id as an argument and stops it using the docker stop command."""
    subprocess.run(["docker", "stop", container_id])


def stop_all_containers(save=True):
    """Stops all containers, except for the currently running gio servers. If the save parameter is set to True, it saves the container IDs to a JSON file. It uses a ThreadPoolExecutor to submit a stop_container function for each container ID in the list."""
    output = subprocess.run(["docker", "ps", "-q"], capture_output=True)
    container_ids = output.stdout.decode().strip().split("\n")

    # Currently running gio servers mustnt be stopped
    container_ids = [item for item in container_ids if item not in gio_containers_ids]

    # An empty container_ids list could mean that containers are already running, which means gio is active
    if (save and len(container_ids) != 0):
        with open(get_local_json_file_path("containers.json"), "w") as f:
            json.dump(container_ids, f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(stop_container, container_id) for container_id in container_ids]
        concurrent.futures.wait(futures)


def start_container(container_id):
    """Takes a container as an argument and starts it using the docker start command."""
    subprocess.run(["docker", "start", container_id])


def start_stopped_containers():
    """Starts all containers whose ids are stored in a json file. It does this by loading the container ids from the json file, then running a docker start command for each one in parallel using concurrent.futures.ThreadPoolExecutor()."""
    with open(get_local_json_file_path("containers.json")) as f:
        container_ids = json.load(f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(start_container, container_id) for container_id in container_ids]
        concurrent.futures.wait(futures)


def run_with_logging(runner):
    """This function takes in a runner as an argument and runs it with logging. It opens the log file in append mode and passes it to the runner. The runner is responsible for writing to the log file."""
    with open(log_file, 'a') as f:
        runner(f)
