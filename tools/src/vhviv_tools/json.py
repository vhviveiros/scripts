import inspect
import json as s_json
from vhviv_tools.file import get_local_file_path


def json(file: str):
    """Takes in a filename as a string and returns the contents of the file as a JSON object. It uses the json library to load the file from the local file path given by get_local_file_path()."""
    with open(get_local_file_path(file, inspect.currentframe().f_back)) as f:
        return s_json.load(f)
