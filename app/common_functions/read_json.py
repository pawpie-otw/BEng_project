from json import load as json_load
from typing import Union
from pathlib import Path


def read_json_file(path_to_json_file: Union[str, Path]) -> dict:
    """Read json file and return converted it to python dict.

    Args:
        path_to_json_file (Union[str, Path]): Path to file.

    Returns:
        dict: json file converted to python dict.
    """
    return dict(json_load(open(path_to_json_file, encoding="utf8")))
