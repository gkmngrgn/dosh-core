import urllib.request

from dosh.commands import external as cmd


def test_copy(tmp_path):
    (tmp_path / "foo" / "bar" / "baz").mkdir(parents=True)
    (tmp_path / "foo" / "bar" / "meow.py").touch()
    (tmp_path / "foo" / "bar" / "baz" / "hell.txt").touch()

    src = str(tmp_path / "foo" / "*")
    dst = str(tmp_path / "dst")
    cmd.copy(src, dst)

    assert (tmp_path / "dst" / "bar" / "meow.py").exists()
    assert (tmp_path / "dst" / "bar" / "baz" / "hell.txt").exists()

    # try overwrite
    cmd.copy(src, dst)


def test_run():
    result = cmd.run("echo Hello, World!")
    assert result.status == cmd.CommandStatus.OK
    assert result.response == "Hello, World!"


def test_run_url(httpserver):
    sh_content = 'echo "Hello, World!"'
    httpserver.expect_request("/hello.sh").respond_with_data(
        sh_content, content_type="text/plain"
    )
    url = httpserver.url_for("/hello.sh")

    with urllib.request.urlopen(url) as response:
        content = response.read()

    assert content.decode("utf-8") == sh_content

    result = cmd.run_url(url)
    assert result.status == cmd.CommandStatus.OK
    assert result.response is not None
    assert result.response.stdout.decode("utf-8") == "Hello, World!\n"


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
