"""DOSH CLI app."""
import sys
from argparse import SUPPRESS, ArgumentParser, RawTextHelpFormatter
from typing import Final

from dosh.logger import set_verbosity
from dosh.parser import get_config_parser

RESERVED_COMMANDS: Final = ["help", "init"]


class CLI:
    """DOSH command line interface."""

    def __init__(self) -> None:
        """Initialize cli with config parser."""
        self.conf_parser = get_config_parser()
        self.arg_parser = self.get_argument_parser()

    def get_argument_parser(self) -> ArgumentParser:
        """Create parser for parsing arguments."""
        parser = ArgumentParser(
            prog=__package__,
            formatter_class=RawTextHelpFormatter,
            description=self.conf_parser.get_description(),
            epilog=self.conf_parser.get_epilog(),
            usage=SUPPRESS,
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="set verbosity for printing logs by level",
        )

        subparsers = parser.add_subparsers()

        # init command
        parser_init = subparsers.add_parser("init", help="initialize a new dosh config")
        parser_init.set_defaults(func=self.parse_init)

        commands = self.conf_parser.get_commands()
        for cmd, help_text in commands.items():
            subparsers.add_parser(cmd, help=help_text)

        return parser

    def parse_command(self) -> None:
        """Parse user-defined commands."""
        self.conf_parser.run_command(sys.argv[1])

    def parse_init(self) -> None:
        """Initialize a new dosh configuration."""
        print("parse init")

    def config_exists(self) -> bool:
        """Return dosh configuration file existency."""
        return self.conf_parser.content is not None

    def run(self) -> None:
        """Run cli reading the arguments."""
        args = self.arg_parser.parse_args()
        set_verbosity(verbosity=args.verbose)

        if not hasattr(args, "func"):
            self.arg_parser.print_help()
            return

        args.func()


def run() -> None:
    """Run command line interface app."""
    cli = CLI()

    if cli.config_exists():
        cli.run()
    else:
        print("Config file doesn't exist.")
