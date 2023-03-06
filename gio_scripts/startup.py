from shared import start_container, stop_all_containers, subprocess, json, get_local_file_path

with open(get_local_file_path("processes_to_finish.json")) as f:
    processes_to_finish = json.load(f)

containers_to_start = ["mysql", "redis", "loginserver", "nodeserver", "dispatch", "dbgate", "gameserver", "gateserver"]

"""This function kills the process with the given name. It first runs a tasklist command to get a list of all running processes with the given name, then extracts the process IDs from the output, and finally kills each process using a taskkill command."""


def kill_process(name):
    # Get a list of all running processes with the given name
    p = subprocess.run(["/mnt/c/Windows/System32/tasklist.exe", "/fi", "IMAGENAME eq " + name], stdout=subprocess.PIPE)

    # Extract the process IDs from the output
    pids = [line.split()[1] for line in p.stdout.decode().splitlines()[3:]]

    # Kill each process
    for pid in pids:
        subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/F", "/T", "/PID", pid])


stop_all_containers()
[kill_process(process) for process in processes_to_finish]
[start_container(container) for container in containers_to_start]
