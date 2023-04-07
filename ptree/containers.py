"""This module contains implemntation of Container class and its subclasses."""


import pathlib


class Container:
    """Stores files and folders represented as pathlib.Path object."""

    def __init__(self):
        self._container = list()

    @property
    def container(self):
        return self._container

    def append(self, value: pathlib.Path):
        self._container.append(value)


class DirsContainer(Container):
    """Stores folders represented as pathlib.Path object."""

    def del_dot_dirs(self):
        dot_dirs = (
                ".git",
                ".env",
                )
        dot_dirs = tuple(map(pathlib.Path, dot_dirs))
        self._container = list(filter(
            lambda d: d not in dot_dirs, self._container
            ))


class FilesContainer(Container):  
    """Stores files represented as pathlib.Path object."""
    pass
