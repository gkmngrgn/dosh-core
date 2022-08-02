# DOSH

Shell-independent command manager. Create your `dosh.star` file in the
project folder and define your tasks, aliases, environments. Dosh will
work like a CLI app reading your config file.


## ENVIRONMENT VARIABLES

#### OPERATING SYSTEM TYPE CHECKING: `IS_LINUX` - `IS_MACOS` - `IS_WINDOWS`

OS type variables to detect your current operating system. All
variables return `True` or `False`. You can find many examples of use
of these variables in the documentation.


#### SHELL TYPE CHECKING: `IS_BASH` - `IS_PWSH` - `IS_ZSH`

Your current shell. All these variables return `True` or `False`. It's
useful if you use shell-specific package like `ohmyzsh`.


## FUNCTIONS

#### GENERAL PURPOSE: `clone`, `eval` - `eval_url`

The main purpose of dosh to write one script that works on multiple
operating systems and shells. But it has to have a limit and it's
nonsense to define functions for each command. So if you want to run a
cli app (like `exa`, `bat`, `helix`, etc.), then you can use `eval`
for it:

```python
eval("helix")

if IS_MACOS or IS_LINUX:
    eval_url("https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh")

if IS_WINDOWS:
    clone("https://github.com/coreybutler/nvm-windows.git")
```

#### FILE SYSTEM OPERATIONS: `path`, `path_home`, `copy`

There are some ready-made functions both to keep the code readable and
to make it work the same in every operating system. You know Windows
prefers backslash as a path separator. This code will work on all
operating systems:

```python
if path_home() == path("/Users/goedev"):
    copy(path_home("Workspace/goedev/emacs.d"), path_home(".emacs.d"))
```


#### INSTALLATION: `brew_install`, `apt_install`, `winget_install`

TODO...


#### FILE, FOLDER, COMMAND EXISTENCY: `exists`, `exists_command`

TODO...


#### LOGGING: `debug` - `info` - `warning` - `error`

TODO...


## EXAMPLE CONFIGURATION

```python
REPOS_DIR = path_home("Workspace/goedev")
CONFIG_REPO_DIR = path(REPOS_DIR + "/config")


def cmd_setup_my_os():
    """place my config files."""

    info("replace my config folder and home files.")
    copy(path(CONFIG_REPO_DIR + "/config/*"), path_home(".config"))
    copy(path(CONFIG_REPO_DIR + "/tmp/home/.*"), path_home())

    if IS_ZSH and not exists(path_home(".oh-my-zsh")):
        debug("ohmyzsh is not installed yet.")
        eval_url("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")

    clone("https://github.com/tmux-plugins/tpm", target=path_home(".tmux/plugins/tpm"), fetch=True)


def cmd_install_cli_apps():
    """install my favorite apps."""

    if IS_MACOS:
        packages = ["git", "ripgrep", "bat", "exa", "miniconda", "emacs"]
        brew_install(packages, cask=True)

    elif IS_LINUX:
        packages = ["git", "ripgrep", "bat", "exa", "alacritty"]
        apt_install(packages)

    elif IS_WINDOWS:
        packages = ["Git.Git", "Microsoft.WindowsTerminal", "Microsoft.VisualStudioCode"]
        winget_install(packages)

    else:
        error("What the hell are you using??")


def cmd_sync_repos(repo_path):
    """
    don't forget to push your changes before working on a different laptop.

    repo_path: str, optional
    """
    if repo_path:
        repo_dirs = [repo_path]
    else:
        repo_dirs = get_folders(REPOS_DIR)

    for repo_dir in repo_dirs:
        result = sync(repo_dir)
        if result.status != STATUS_OK:
            error(result.message)
```

## WHAT IF YOU TRY TO USE THIS CONFIG...

After you created your `dosh.star` file, you can see all available
tasks with the command `dosh help`:

```shell
$ dosh help  # or just dosh
Tasks:
  > setup_my_os        place my config files.
  > install_cli_apps   install my favorite apps.
  > sync_repos         don't forget to push your changes before working on a different
                       laptop.
                       - repo_path: str, optional

$ dosh install_cli_apps
...

$ dosh sync_repos -- repo_path=yank
...
```


## QUESTIONS

### CAN I TRUST THIS PROJECT?

No. Don't trust any project. The source code is open, trust yourself
and read the code.


### BUT DO YOU USE THIS PROJECT YOURSELF?

Yes, I use multiple operating systems with different shells, and I'm
too tired to write my scripts in multiple languages. This is why I
created this project.


### WHY DOESN'T DOSH HAVE ANY REMOVE COMMAND?

Because it's too dangerous! I don't use any remove command in my
scripts indeed. If you really need a remove command, you can run it
with `eval`. But remember, contributors of this project don't
guarantee anything.


### IS THERE ANY SYNTAX HIGHLIGHTER, EDITOR EXTENSION, OR LINTER FOR D...

Open your `dosh.star` file in your favorite editor with Python -
Bazel - Starlark mode and just write your f*cking script now.  Or take
a look at this link:
https://github.com/bazelbuild/starlark/blob/master/users.md
