import datetime
import shutil
import os
from shared import logs_folder, run_with_logging


def runner(f):
    """This code iterates through each file in a given directory (logs_folder) and attempts to delete it. If the file is a regular file or symbolic link, it will be deleted using os.unlink(). If the file is a directory, it will be deleted using shutil.rmtree(). If an error occurs while deleting the file, an error message will be written to a log file."""
    f.write(f"[EVENT] [{datetime.datetime.now()}] Starting Log Cleaning Process...\n")
    for filename in os.listdir(logs_folder):
        file_path = os.path.join(logs_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                f.write(f"[DELETE FILE] [{datetime.datetime.now()}] Deleted file {file_path}\n")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                f.write(f"[DELETE DIR] [{datetime.datetime.now()}] Deleted directory {file_path}\n")
        except Exception as e:
            f.write(f"[ERROR] [{datetime.datetime.now()}] Failed to delete {file_path}. Reason: {e}\n")
    f.write(f"[EVENT] [{datetime.datetime.now()}] Log Cleaning Process finished.\n")

run_with_logging(runner)
