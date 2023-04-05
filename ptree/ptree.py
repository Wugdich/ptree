"""This module provides ptree main module."""

import os
import pathlib
import sys
from collections import deque
from typing import TextIO


PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


# TODO: add support sorting files and directories
# TODO: add icons and colors to the tree diagram
# TODO: set up the application to publish it as an open source project
# TODO: add directories and files counter
class DirectoryTree:
    """Class creates the directory tree diagram
    and steam it to the setted output file.
    """

    def __init__(
        self,
        root_dir: str | pathlib.Path,
        dir_only: bool = False,
        output_file: TextIO | str = sys.stdout,
        strict: bool = False
    ):
        self._generator = _TreeGenerator(root_dir, dir_only, strict)
        self._output_file = output_file

    def generate(self):
        """Generates each building block of diagram and print it to the
        setted stream.
        """
        tree = self._generator.build_tree()
        if self._output_file != sys.stdout:
            tree.appendleft("```")
            tree.append("```")
            self._output_file = open(
                    self._output_file, mode="w", encoding="UTF-8"
                    )
        with self._output_file as stream:
            for entry in tree:
                print(entry, file=stream)


class _TreeGenerator:
    """Class traverses the file system and generates the directory tree
    diagram.
    """

    def __init__(
            self, 
            root_dir: str | pathlib.Path,
            dir_only: bool = False,
            strict: bool = False
            ):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._strict = strict
        self._tree = deque()

    def build_tree(self) -> deque[str]:
        """Generates and returns the directory tree diagram."""
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """Build a head of the tree."""
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory: pathlib.Path, prefix: str = ""):
        """Build a body of the tree."""
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        """Prepares entries according directory only argument"""
        entries = directory.iterdir()
        directories = list()
        files = list()
        for entry in entries:
            if entry.is_file():
                files.append(entry)
            else:
                directories.append(entry)
        directories = self._apply_directories_filter(directories)
        if self._dir_only:
            return directories
        entries = sorted(
                directories + files, 
                key=lambda entry: entry.is_file()
                )
        return entries

    def _apply_directories_filter(
            self,
            directories: list[pathlib.Path]
            ) -> list[pathlib.Path]:
        """Reads directories' filter flags and apllies its"""
        if not self._strict:
            restricted_dirs = (".git", "venv")
            restricted_dirs_paths = tuple(map(pathlib.Path, restricted_dirs))
            directories = list(filter(
                lambda d: d not in restricted_dirs_paths, directories
                ))
        return directories

    def _add_directory(
        self,
        directory: pathlib.Path,
        index: int,
        entries_count: int,
        prefix: str,
        connector: str,
    ):
        """Appends a new directory to the list represented a tree diagram."""
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory=directory, prefix=prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str):
        """Appends a new file to the list represented a tree diagram."""
        self._tree.append(f"{prefix}{connector} {file.name}")
