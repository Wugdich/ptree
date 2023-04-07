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
    tree = DirectoryTree(
            root_dir, 
            dir_only=args.dir_only, 
            output_file=args.output_file,
            strict=args.strict
            )
    tree.generate()

# TODO: prettify help output
def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
            prog="ptree",
            description=("ptree, a directory tree generator "
                         "implemented in python"),
            epilog="Thanks for using ptree!",
            )
    parser.version = f"ptree v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
            "root_dir", 
            metavar="ROOT_DIR",
            nargs="?",
            default=".",
            help="Generate a full directory tree starting at ROOT_DIR",
            )
    parser.add_argument(
            "-d",
            "--dir-only",
            action="store_true",
            help="Generate a directory-only tree",
            )
    parser.add_argument(
            "-o",
            "--output-file",
            metavar="OUTPUT_FILE",
            nargs="?",
            default=sys.stdout,
            help="Generate a full directory tree and save it to a file",
            )
    parser.add_argument(
            "-s",
            "--strict",
            action="store_true",
            help="Stop ignoring directories like '.git', 'venv'"
            )
    return parser.parse_args()
