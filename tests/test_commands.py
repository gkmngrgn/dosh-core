import os

from dosh.commands import env


def test_environments():
    key_ = "DOSH_ENV"
    os.environ[key_] = "production"
    assert env(key_) == "production"

    del os.environ[key_]
    assert env(key_) == ""
