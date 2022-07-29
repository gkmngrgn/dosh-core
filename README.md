# DOSH

Shell-independent command manager. Create your `dosh.star` file in the
project folder and define your tasks, aliases, environments. Dosh will
work like a CLI app reading your config.


## USAGE

After you created your `dosh.star` file, you can see all available
tasks with the command `dosh` or `dosh help`:

```shell
$ dosh help

Tasks:
  > build                  build your project.
  > shell                  log in to docker shell.
  > update_translations    update django translation files.
    params: langs=str(en|de|tr)
            fuzzy=bool

$ dosh build

$ dosh update_translations -- langs=en,de,tr fuzzy=false
...
```

## ENVIRONMENT VARIABLES

#### `IS_LINUX` - `IS_MACOS` - `IS_WINDOWS`

OS type variables to detect your current operating system.

#### `IS_BASH` - `IS_PWSH` - `IS_ZSH`

Your current shell.


## FUNCTIONS

- `brew_install`

- `copy`

- `env`

- `eval`

- `exists, type={file_or_directory(default),command}`

- `home_dir`

- `print`

- `sync`


## EXAMPLE CONFIGURATION

```python
# dosh.star

def cmd_setup_my_os():
    """Place my config files."""

    clone(url="https://github.com/gkmngrgn/config", folder=home_dir("tmp"))
    copy(home_dir("tmp/config/*"), home_dir(".config"))
    copy(home_dir("tmp/home/.*"), home_dir())

    if IS_ZSH and not exists(home_dir(".oh-my-zsh")):
        eval_url("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")

    clone(
        url="https://github.com/tmux-plugins/tpm",
        folder=home_dir(".tmux/plugins/tpm"),
        sync=True,
    )


def cmd_install_cli_apps():
    """Install my favorite apps."""

    if IS_MACOS:
        brew_install("git", "ripgrep", "bat", "exa")

    elif IS_LINUX:
        apt_install("git", "ripgrep", "bat", "exa")

    elif IS_WINDOWS:
        winget_install("git", "ripgrep", "bat", "exa")

    else:
        print("What the hell are you using??")
```


## QUESTIONS

### WHY DOESN'T DOSH HAVE ANY REMOVE COMMAND?

Because it's too dangerous! Even the authors and contributors of this
project don't guarantee anything. If you really need a remove command,
you can run it with `eval`.
