def cmd_compile():
    """Build the project."""
    run("pyoxidizer build")


def cmd_test():
    """Run all unit tests."""
    run("python -m unittest discover")


def cmd_run():
    """Run dosh without installing."""
    run("python -m dosh.cli")


def cmd_lint():
    """Run linters."""
    run("pre-commit run --all-files")
