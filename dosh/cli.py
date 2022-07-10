"""DOSH CLI app."""

import sys
from argparse import ArgumentParser, Namespace
from typing import Final

from dosh.help import generate_help
from dosh.parser import get_config_parser

RESERVED_COMMANDS: Final = ["help", "init"]


class CLI:
    """DOSH command line interface."""

    def __init__(self) -> None:
        """Initialize cli with config parser."""
        self.config_parser = get_config_parser()

    def parse_arguments(self) -> Namespace:
        """Parse sub commands and generate help output."""
        parser = ArgumentParser(
            prog=__package__,
            description="Shell-independent command manager.",
        )
        subparsers = parser.add_subparsers()

        # help command
        parser_help = subparsers.add_parser("help")
        parser_help.set_defaults(func=self.parse_help)

        # init command
        parser_init = subparsers.add_parser("init")
        parser_init.set_defaults(func=self.parse_init)

        return parser.parse_args()

    def parse_command(self) -> None:
        """Parse user-defined commands."""
        self.config_parser.run_command(sys.argv[1])

    def parse_help(self) -> None:
        """Print help output."""
        commands = self.config_parser.get_commands()
        output = generate_help(commands)
        print(output)

    def parse_init(self) -> None:
        """Initialize a new dosh configuration."""
        print("parse init")

    def config_exists(self) -> bool:
        """Return dosh configuration file existency."""
        return self.config_parser.content is not None

    def run(self) -> None:
        """Run cli reading the arguments."""
        if len(sys.argv) == 1:
            self.parse_help()
        else:
            cmd = sys.argv[1]

            if cmd not in RESERVED_COMMANDS and not cmd.startswith("-"):
                self.parse_command()
            else:
                parsed_args = self.parse_arguments()
                parsed_args.func()


def run() -> None:
    """Run command line interface app."""
    cli = CLI()

    if cli.config_exists():
        cli.run()
    else:
        print("Config file doesn't exist.")
