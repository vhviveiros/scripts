import inspect
import os


def get_local_file_path(file_name: str, frame=None) -> str:
    """This function takes in a file name (str) and an optional frame (default None) and returns the absolute path of the file name. It uses the inspect module to get the file name of the module and then uses os.path.dirname() to get the absolute path of the file name. Finally, it uses os.path.join() to construct the path of the json file and returns it."""
    # Get the file name of the module
    if frame is None:
        file = inspect.getframeinfo(inspect.stack()[1][0]).filename
    else: 
        file = inspect.getmodule(frame).__file__

    # Get the absolute path of the file name
    script_dir = os.path.dirname(file)

    # construct the path of the json file
    return os.path.join(script_dir, file_name)
