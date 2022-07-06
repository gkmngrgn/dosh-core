"""DOSH CLI app."""

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from dosh.help import generate_help

CONFIG_FILENAME = "dosh.bzl"
RESERVED_COMMANDS = ["help", "init"]


def parse_command() -> None:
    print(sys.argv)
    print("parse command")


def parse_help() -> None:
    output = generate_help()
    print(output)


def parse_init() -> None:
    print("parse init")


class CLI:
    def __init__(self) -> None:
        self.config_file = self.__find_config_file()

    def __find_config_file(self) -> Path:
        """
        Return file path of dosh script.

        TODO: Improve this function to find the file in a different folder.
        """
        return Path.cwd() / CONFIG_FILENAME

    def parse_arguments(self) -> Namespace:
        parser = ArgumentParser(
            prog=__package__,
            description="Shell-independent command manager.",
        )
        subparsers = parser.add_subparsers()

        # help command
        parser_help = subparsers.add_parser("help")
        parser_help.set_defaults(func=parse_help)

        # init command
        parser_init = subparsers.add_parser("init")
        parser_init.set_defaults(func=parse_init)

        return parser.parse_args()

    def config_exists(self) -> bool:
        return self.config_file.exists()

    def run(self) -> None:
        if len(sys.argv) == 1:
            parse_help()
        else:
            cmd = sys.argv[1]

            if cmd not in RESERVED_COMMANDS and not cmd.startswith("-"):
                parse_command()
            else:
                parsed_args = self.parse_arguments()
                parsed_args.func()


def validate_config_file() -> None:
    pass


def eval_config_file() -> None:
    pass


def run() -> None:
    cli = CLI()

    if cli.config_exists():
        cli.run()
    else:
        print("Config file doesn't exist.")


if __name__ == "__main__":
    run()
