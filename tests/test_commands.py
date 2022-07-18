import os
from contextlib import redirect_stdout
from io import StringIO

from dosh import commands as cmd


def test_command_env():
    key_ = "DOSH_ENV"
    os.environ[key_] = "production"
    assert cmd.env(key_) == "production"

    del os.environ[key_]
    assert cmd.env(key_) == ""


def test_command_eval():
    result = cmd.eval("echo Hello, World!")
    assert result.stdout == b"Hello, World!\n"
