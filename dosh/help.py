"""Help output generator."""


def generate_help() -> str:
    """
    Generate a help output looking at available commands.
    """
    output = """
Subcommands:
  > install            copy your configuration files to your home folder.
  > install_cli_apps   install cli apps.
    """
    return output
