import subprocess
import datetime
from shared import mysql_folder, redis_folder, run_with_logging


backup_root = '/mnt/d/GAME/Genshin Impact GIO'
backup_mysql = backup_root + '/backup/mysql/'
backup_redis = backup_root + '/backup/redis/'


def backup_folder(local_folder: str, backup_folder: str) -> None:
    """This function takes two strings as parameters, a local folder and a backup folder, and backs up the local folder to the backup folder. It uses the rsync command to perform the backup, excluding mysql.sock from the backup process. The function also logs events and errors in a log file. If an error occurs during the backup process, it is logged in the log file."""
    def runner(f):
        f.write(f"[EVENT] [{datetime.datetime.now()}] Starting Backup Process for {local_folder}...\n")
        try:
            subprocess.run(["rsync", "-av", "--delete", "--exclude", "mysql.sock", local_folder, backup_folder], check=True)
        except subprocess.CalledProcessError as e:
            f.write(f"[ERROR] [{datetime.datetime.now()}] Backup Process for {local_folder} has failed. Error: {e}\n")
        finally:
            f.write(f"[EVENT] [{datetime.datetime.now()}] Backup Process for {local_folder} finished.\n")
    run_with_logging(runner)

backup_folder(mysql_folder, backup_mysql)
backup_folder(redis_folder, backup_redis)
