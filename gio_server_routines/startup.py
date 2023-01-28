from shared import subprocess, start_container, stop_all_containers

processes_to_finish = ["QuickLook.exe", "Taskmgr.exe", "WhatsApp.exe",
                       "Video.UI.exe", "msedgewebview2.exe", "msrdc.exe", "TranslucentTB.exe", "hide_desktop_icons.exe", "GoogleDriveFS.exe", "PhoneExperienceHost.exe", "CC_Engine_x64.exe", "PowerToys.exe", "wallpaper64.exe", "MSI.CentralServer.exe", "MSI_Central_Service.exe", "MSI_Companion_Service.exe", "OfficeClickToRun.exe", "LEDKeeper2.exe", "spd.exe", "LEDKeeper2.exe"]

containers_to_start = ["mysql", "redis", "loginserver", "nodeserver", "dispatch", "dbgate", "gameserver", "gateserver"]


def kill_process(name):
    # Get a list of all running processes with the given name
    p = subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/FI", "imagename eq " + name], stdout=subprocess.PIPE)

    # Extract the process IDs from the output
    pids = [line.split()[1] for line in p.stdout.decode().splitlines()[3:]]

    # Kill each process
    for pid in pids:
        subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/F", "/T", "/PID", pid])


stop_all_containers()
[kill_process(process) for process in processes_to_finish]
[start_container(container) for container in containers_to_start]
