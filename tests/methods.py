import pathlib


def count_files(path: pathlib.Path, name: str = "*.*"):
    return len(list(pathlib.Path(path).glob(name)))