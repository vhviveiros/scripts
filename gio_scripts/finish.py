import sys
from shared import stop_all_containers, start_stopped_containers, subprocess

stop_all_containers(save=False)
start_stopped_containers()
subprocess.run(["netsh.exe", "winhttp", "reset", "proxy"])
if (sys.argv.__contains__('-s')):
    subprocess.run(["shutdown.exe", "-s", "-t", "10"])
subprocess.run(["wsl.exe", "--shutdown"])
