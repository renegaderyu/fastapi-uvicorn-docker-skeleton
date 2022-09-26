import os

from app.models import Example


def remove_file(path: str) -> None:
    os.unlink(path)


def do_something(example: Example, tmp_file: str):
    with open(tmp_file, "w+") as f:
        f.write("{} = {}\n".format(example.name, example.value))
    return tmp_file
