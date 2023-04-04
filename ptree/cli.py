"""This module provides the ptree cli interface."""


import argparse
import pathlib
import sys


from . import __version__
from .ptree import DirectoryTree

def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print(f"{root_dir!r} directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(root_dir)
    tree.generate()
