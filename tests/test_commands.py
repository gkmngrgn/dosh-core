import os
import pathlib
import urllib.request
from pathlib import Path

import pytest

from dosh_core.commands import external as cmd
from dosh_core.commands.base import CommandException, normalize_path
from dosh_core.logger import get_logger, set_verbosity

logger = get_logger()


def test_copy(tmp_path):
    (tmp_path / "foo" / "bar" / "baz").mkdir(parents=True)
    (tmp_path / "foo" / "bar" / "meow.py").touch()
    (tmp_path / "foo" / "bar" / "baz" / "hell.txt").touch()

    # test with files "foo/*"
    src1 = str(tmp_path / "foo" / "*")
    dst1 = str(tmp_path / "dst1")

    cmd.copy(src1, dst1)
    assert (tmp_path / "dst1" / "bar" / "meow.py").exists()
    assert (tmp_path / "dst1" / "bar" / "baz" / "hell.txt").exists()

    # try overwrite, we don't expect to create a folder "foo" in dst1.
    cmd.copy(src1, dst1)
    assert not (tmp_path / "dst1" / "foo").exists()

    # test with a folder name "foo"
    src2 = str(tmp_path / "foo")
    dst2 = str(tmp_path / "dst2")

    cmd.copy(src2, dst2)
    assert (tmp_path / "dst2" / "bar" / "meow.py").exists()
    assert (tmp_path / "dst2" / "bar" / "baz" / "hell.txt").exists()

    # try overwrite, we expect to create a folder "foo" in dst2.
    cmd.copy(src2, dst2)
    assert (tmp_path / "dst2" / "foo" / "bar" / "meow.py").exists()
    assert (tmp_path / "dst2" / "foo" / "bar" / "baz" / "hell.txt").exists()


def test_run(caplog):
    set_verbosity(3)
    result = cmd.run("echo Hello, World!")
    assert result == os.EX_OK
    assert caplog.records[0].message == "[RUN] echo Hello, World!"
    assert caplog.records[1].message == "Hello, World!"


def test_run_url(httpserver, caplog):
    set_verbosity(3)

    sh_content = 'echo "Hello, World!"'
    httpserver.expect_request("/hello.sh").respond_with_data(
        sh_content, content_type="text/plain"
    )
    url = httpserver.url_for("/hello.sh")

    with urllib.request.urlopen(url) as response:
        content = response.read()

    assert content.decode("utf-8") == sh_content

    result = cmd.run_url(url)
    assert result == os.EX_OK
    assert (
        caplog.records[2].message
        == f"[RUN_URL] http://{httpserver.host}:{httpserver.port}/hello.sh"
    )
    assert caplog.records[3].message == "Hello, World!"


def test_exists(tmp_path):
    src_path1 = tmp_path / "this-file-does-not-exist.txt"
    assert not cmd.exists(str(src_path1))

    src_path2 = tmp_path / "this-file-exists.txt"
    src_path2.touch()
    assert cmd.exists(str(src_path2))

    src_path3 = tmp_path / "this" / "folder" / "exists"
    src_path3.mkdir(parents=True)
    assert cmd.exists(str(src_path3))


def test_exists_command():
    assert cmd.exists_command("bash")
    assert not cmd.exists_command("hsab")


def test_normalize_path(monkeypatch):
    monkeypatch.setenv("HOME", "/home/dosh")

    assert normalize_path("~/.config") == Path("/home/dosh/.config")
    assert normalize_path("/foo/bar/baz") == Path("/foo/bar/baz")
    assert normalize_path("current_dir") == Path.cwd() / "current_dir"


def test_scan_directory():
    cwd = pathlib.Path.cwd()

    # test current working directory
    result = cmd.scan_directory()
    assert result is not None
    assert str(cwd / "README.md") in list(result.values())

    # test examples directory
    result = cmd.scan_directory("./tests")
    assert result is not None
    assert list(result.values()) == [
        str(cwd / "tests" / file_name)
        for file_name in [
            "__pycache__",
            "test_commands.py",
            "test_logger.py",
            "test_task.py",
        ]
    ]

    # test invalid directory
    with pytest.raises(CommandException) as excinfo:
        cmd.scan_directory("./README.md")
        assert str(excinfo.value) == "Not a folder: ./README.md"
