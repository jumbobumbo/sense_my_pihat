from json import load
from pathlib import Path

def load_json(*args, parent_dir: str = 'patterns'):
    """
    loads json file from a 'parent' DIR, supports sub DIRs
    param: args: str (sub dirs and file under parent DIR)
    param: parent_dir: str - Parent folder of your json files
    """
    file_path = Path(parent_dir)
    for arg in args:
        file_path = Path.joinpath(file_path, arg)

    with open(file_path, "r") as f:
        return load(f)
