from shared import stop_all_containers, start_stopped_containers, subprocess

stop_all_containers(save=False)
start_stopped_containers()
subprocess.run(["wsl.exe", "--shutdown"])