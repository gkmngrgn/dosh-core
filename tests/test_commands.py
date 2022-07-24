import os

from dosh import commands as cmd


def test_copy(tmp_path):
    (tmp_path / "foo" / "bar" / "baz").mkdir(parents=True)
    (tmp_path / "foo" / "bar" / "meow.py").touch()
    (tmp_path / "foo" / "bar" / "baz" / "hell.txt").touch()

    src = str(tmp_path / "foo" / "*")
    dst = str(tmp_path / "dst")
    cmd.copy(src, dst)

    assert (tmp_path / "dst" / "bar" / "meow.py").exists()
    assert (tmp_path / "dst" / "bar" / "baz" / "hell.txt").exists()


def test_env():
    key_ = "DOSH_ENV"
    os.environ[key_] = "production"
    assert cmd.env(key_) == "production"

    del os.environ[key_]
    assert cmd.env(key_) == ""


def test_eval():
    result = cmd.eval("echo Hello, World!")
    assert result.stdout == b"Hello, World!\n"


def test_exists(tmp_path):
    src_path1 = tmp_path / "this-file-does-not-exist.txt"
    assert not cmd.exists(str(src_path1))

    src_path2 = tmp_path / "this-file-exists.txt"
    src_path2.touch()
    assert cmd.exists(str(src_path2))

    src_path3 = tmp_path / "this" / "folder" / "exists"
    src_path3.mkdir(parents=True)
    assert cmd.exists(str(src_path3))


def test_home_dir():
    # I want to run tests on my locale so there's no common solution to define home
    # statically. However, I can be sure that the home is not empty.
    home = os.getenv("HOME")
    assert isinstance(home, str)
    assert len(home) > 0

    # FIXME: separator will be a problem on Windows.
    assert cmd.home_dir() == home
    assert cmd.home_dir("foo/bar/baz") == f"{home}/foo/bar/baz"
