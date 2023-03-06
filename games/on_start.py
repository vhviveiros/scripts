from vhviv_tools.json import json

from tools.src.vhviv_tools.process import kill_processes


process_to_finish = json('config.json')['processes_to_finish']
kill_processes(process_to_finish)