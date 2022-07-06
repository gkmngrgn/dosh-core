def cmd_compile():
    run("pyoxidizer build")


def cmd_test():
    run("python -m unittest discover")


def cmd_run():
    run("python -m dosh.cli")
