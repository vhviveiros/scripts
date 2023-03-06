import subprocess


def get_process_ids(name):
    # Get a list of all running processes with the given name
    p = subprocess.run(["/mnt/c/Windows/System32/tasklist.exe", "/fi", "IMAGENAME eq " + name], stdout=subprocess.PIPE)

    # Extract the process IDs from the output
    return [line.split()[1] for line in p.stdout.decode().splitlines()[3:]]


def kill_process(name):
    # Get a list of all running processes with the given name and kill them one by one
    for pid in get_process_ids(name):
        subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/F", "/T", "/PID", pid])


def kill_processes(names):
    for p in names:
        kill_process(p)

#TODO: kill wsl