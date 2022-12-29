import platform

from dosh.commands.base import CommandResult, CommandStatus, OperatingSystem, Task
from dosh.config import ConfigParser


def test_get_current_operating_system(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert OperatingSystem.get_current() == OperatingSystem.MACOS

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert OperatingSystem.get_current() == OperatingSystem.LINUX

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert OperatingSystem.get_current() == OperatingSystem.WINDOWS

    monkeypatch.setattr(platform, "system", lambda: "FreeBSD")
    assert OperatingSystem.get_current() == OperatingSystem.UNSUPPORTED


def test_task_if_available_on_linux(monkeypatch, caplog, capsys):
    def print_hello():
        print("hello")
        return CommandResult(CommandStatus.OK)

    task_hello = Task(
        name="hello",
        required_platforms=["windows", "macos"],
        command=print_hello,
    )
    config_parser = ConfigParser(content="")
    config_parser.tasks = [task_hello]

    # run task on unsupported operating system first.
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    config_parser.run_task("hello", params=[])

    assert len(caplog.records) == 1
    assert capsys.readouterr().out == ""
    assert (
        caplog.records[0].message
        == "The task `hello` does not work on this operating system."
    )

    # run task on macos. that should be worked.
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    config_parser.run_task("hello", params=[])

    assert len(caplog.records) == 1
    assert capsys.readouterr().out == "hello\n"
