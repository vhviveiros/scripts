import os
import time
import subprocess
import datetime

local_mysql = '/mnt/c/Users/vhviv/APPS/docker-hk4e/data/mysql/'
local_redis = '/mnt/c/Users/vhviv/APPS/docker-hk4e/data/redis/'
backup_mysql = '/mnt/d/GAME/Genshin Impact GIO/backup/mysql/'
backup_redis = '/mnt/d/GAME/Genshin Impact GIO/backup/redis/'

log_file = '/home/vhviv/SCRIPTS/gio_data_backup/backup.log'


def backup_folder(local_folder: str, backup_folder: str) -> None:
    with open(log_file, 'a') as f:
        f.write(f"[EVENT] [{datetime.datetime.now()}] Starting Backup Process for {local_folder}...\n")
    try:
        subprocess.run(["rsync", "-av", "--delete", "--exclude", "mysql.sock", local_folder, backup_folder], check=True)
        with open(log_file, 'a') as f:
            f.write(f"[EVENT] [{datetime.datetime.now()}] Backup Process for {local_folder} finished.\n")
    except subprocess.CalledProcessError as e:
        with open(log_file, 'a') as f:
            f.write(f"[ERROR] [{datetime.datetime.now()}] Backup Process for {local_folder} has failed. Error: {e}\n")


backup_folder(local_mysql, backup_mysql)
backup_folder(local_redis, backup_redis)
