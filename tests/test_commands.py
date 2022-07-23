import os

from dosh import commands as cmd


def test_env():
    key_ = "DOSH_ENV"
    os.environ[key_] = "production"
    assert cmd.env(key_) == "production"

    del os.environ[key_]
    assert cmd.env(key_) == ""


def test_eval():
    result = cmd.eval("echo Hello, World!")
    assert result.stdout == b"Hello, World!\n"


def test_home_dir():
    # I want to run tests on my locale so there's no common solution to define home
    # statically. However, I can be sure that the home is not empty.
    home = os.getenv("HOME")
    assert isinstance(home, str)
    assert len(home) > 0

    # FIXME: separator will be a problem on Windows.
    assert cmd.home_dir() == home
    assert cmd.home_dir("foo/bar/baz") == f"{home}/foo/bar/baz"
