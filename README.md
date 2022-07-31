# DOSH

Shell-independent command manager. Create your `dosh.star` file in the
project folder and define your tasks, aliases, environments. Dosh will
work like a CLI app reading your config file.


## ENVIRONMENT VARIABLES

#### OPERATING SYSTEM TYPE CHECKING: `IS_LINUX` - `IS_MACOS` - `IS_WINDOWS`

OS type variables to detect your current operating system.


#### SHELL TYPE CHECKING: `IS_BASH` - `IS_PWSH` - `IS_ZSH`

Your current shell.


## FUNCTIONS

#### GENERAL PURPOSE: `clone`, `eval` - `eval_url`

TODO...


#### FILE SYSTEM OPERATIONS: `path`, `path_home`, `copy`

TODO...


#### INSTALLATION: `brew_install`, `apt_install`, `winget_install`

TODO...


#### FILE, FOLDER, COMMAND EXISTENCY: `exists`, `exists_command`

TODO...


#### LOGGING: `debug` - `info` - `warning` - `error`

TODO...


## EXAMPLE CONFIGURATION

```python
REPOS_DIR = path_home("Workspace/goedev")
CONFIG_REPO_DIR = path(REPOS_DIR, "config")


def cmd_setup_my_os():
    """place my config files."""

    info("replace my config folder and home files.")
    copy(path(CONFIG_REPO_DIR, "config/*"), path_home(".config"))
    copy(path(CONFIG_REPO_DIR, "tmp/home/.*"), path_home())

    if IS_ZSH and not exists(path_home(".oh-my-zsh")):
        debug("ohmyzsh is not installed yet.")
        eval_url("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")

    clone("https://github.com/tmux-plugins/tpm", target=path_home(".tmux/plugins/tpm"), fetch=True)


def cmd_install_cli_apps():
    """install my favorite apps."""

    if IS_MACOS:
        brew_install("git", "ripgrep", "bat", "exa", "miniconda", "emacs")

    elif IS_LINUX:
        apt_install("git", "ripgrep", "bat", "exa", "alacritty")

    elif IS_WINDOWS:
        winget_install("Git.Git", "Microsoft.WindowsTerminal", "Microsoft.VisualStudioCode")

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
        status, message = sync(repo_dir)

        if status == STATUS_OK:
            info(message)
        else:
            error(message)
```

## WHAT IF YOU TRY TO USE THIS CONFIG...

After you created your `dosh.star` file, you can see all available
tasks with the command `dosh` or `dosh help`:

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
