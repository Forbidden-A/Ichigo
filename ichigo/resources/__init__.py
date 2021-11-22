import io
import os
import pathlib

resources_path = pathlib.Path(os.path.realpath(__file__)).parent


def get_resource(name: str, mode: str = "r") -> io.TextIOWrapper:
    path = pathlib.Path(f"{resources_path}/{name}")
    if not path.exists:
        raise FileNotFoundError(path)
    return open(path, mode)
