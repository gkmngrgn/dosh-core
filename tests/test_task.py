from dosh.commands.base import CommandResult, CommandStatus, OperatingSystem, Task
from dosh.config import ConfigParser


def test_get_current_operating_system(monkeypatch):
    monkeypatch.setenv("OSTYPE", "darwin-blablabla")
    assert OperatingSystem.get_current() == OperatingSystem.MACOS

    monkeypatch.setenv("OSTYPE", "linux")
    assert OperatingSystem.get_current() == OperatingSystem.LINUX

    monkeypatch.setenv("OSTYPE", "msys")
    assert OperatingSystem.get_current() == OperatingSystem.WINDOWS

    monkeypatch.setenv("OSTYPE", "bsd")
    assert OperatingSystem.get_current() == OperatingSystem.UNSUPPORTED


def test_task_if_available_on_linux(monkeypatch, caplog):
    def print_hello():
        print("hello")
        return CommandResult(CommandStatus.OK)

    monkeypatch.setenv("OSTYPE", "linux")

    task_hello = Task(
        name="hello",
        required_platforms=["windows", "macos"],
        command=print_hello,
    )
    config_parser = ConfigParser(content="")
    config_parser.tasks = [task_hello]
    config_parser.run_task("hello", params=[])

    assert len(caplog.records) == 1

    log_record = caplog.records[0]
    assert (
        log_record.message == "The task `hello` does not work on this operating system."
    )
