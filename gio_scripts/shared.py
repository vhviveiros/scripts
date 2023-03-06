import os
import subprocess
import json
import concurrent.futures


def get_local_file_path(file_name: str) -> str:
    """Takes a file name as an argument and returns the path of the file. It does this by getting the path of the current script and joining it with the file name."""
    # get the path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # construct the path of the json file
    return os.path.join(script_dir, file_name)


config = json.load(open(get_local_file_path("config.json")))
root_folder = config["root_folder"]
mysql_folder = root_folder + config["mysql_folder"]
redis_folder = root_folder + config["redis_folder"]
logs_folder = root_folder + config["logs_folder"]
gio_containers_ids = config["gio_containers_ids"]
log_file = get_local_file_path('scripts_logs.log')


def stop_container(container_id):
    """Takes a container id as an argument and stops it using the docker stop command."""
    subprocess.run(["docker", "stop", container_id])


def stop_all_containers(save=True, kill_gio=False):
    """Stops all containers. If the "save" argument is set to True, the list of container IDs will be saved in a JSON file. If the "kill_gio" argument is set to False, any currently running gio servers will not be stopped. The function uses a ThreadPoolExecutor to concurrently stop each container in the list of container IDs."""
    output = subprocess.run(["docker", "ps", "-q"], capture_output=True)
    container_ids = output.stdout.decode().strip().split("\n")

    if (not kill_gio):
        # Currently running gio servers mustnt be stopped
        container_ids = [item for item in container_ids if item not in gio_containers_ids]

    # An empty container_ids list could mean that containers are already running, which means gio is active
    if (save and len(container_ids) != 0):
        with open(get_local_file_path("containers.json"), "w") as f:
            json.dump(container_ids, f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(stop_container, container_id) for container_id in container_ids]
        concurrent.futures.wait(futures)


def start_container(container_id):
    """Takes a container as an argument and starts it using the docker start command."""
    subprocess.run(["docker", "start", container_id])


def start_stopped_containers():
    """Starts all containers whose ids are stored in a json file. It does this by loading the container ids from the json file, then running a docker start command for each one in parallel using concurrent.futures.ThreadPoolExecutor()."""
    with open(get_local_file_path("containers.json")) as f:
        container_ids = json.load(f)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(start_container, container_id) for container_id in container_ids]
        concurrent.futures.wait(futures)


def run_with_logging(runner):
    """This function takes in a runner as an argument and runs it with logging. It opens the log file in append mode and passes it to the runner. The runner is responsible for writing to the log file."""
    with open(log_file, 'a') as f:
        runner(f)
