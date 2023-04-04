"""This module provides ptree main module."""

import os
import pathlib


PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    """Class creates the directory tree diagram 
    and display it on the screen.
    """
    def __init__(self, root_dir: pathlib.Path, dir_only: bool=False):
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        """Displays each component of the tree diagram on the screen"""
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    """Class traverses the file system and generates the directory tree
    diagram.
    """
    def __init__(self, root_dir: pathlib.Path, dir_only: bool=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = list()

    def build_tree(self) -> list[str]:
        """Generates and returns the directory tree diagram."""
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """Build a head of the tree."""
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory: pathlib.Path, prefix: str=""):
        """Build a body of the tree."""
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                        entry, index, entries_count, prefix, connector
                        )
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        """Prepares entries according directory only argument"""
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    # TODO: add ignoring some directories, like '.git'
    def _add_directory(
            self, directory: pathlib.Path, index: int, 
            entries_count: int, prefix: str, connector: str
            ):
        """Appends a new directory to the list represented a tree diagram."""
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
                directory=directory,
                prefix=prefix
                )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str):
        """Appends a new file to the list represented a tree diagram."""
        self._tree.append(f"{prefix}{connector} {file.name}")
