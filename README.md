# DOSH

Shell-independent command manager. Create your `dosh.star` file in the
project folder and define your tasks, aliases, environments. Dosh will
work like a CLI app reading your config.


## ENVIRONMENT VARIABLES

#### OPERATING SYSTEM TYPE CHECKING: `IS_LINUX` - `IS_MACOS` - `IS_WINDOWS`

OS type variables to detect your current operating system.


#### SHELL TYPE CHECKING: `IS_BASH` - `IS_PWSH` - `IS_ZSH`

Your current shell.


## FUNCTIONS

- `clone`

- `copy`

- `home_dir`

#### INSTALLATION: `brew_install`, `apt_install`, `winget_install`

TODO...


#### FILE, FOLDER, COMMAND EXISTENCY: `exists` - `exists_command`

TODO...


#### EVALUATION: `eval` - `eval_url`

TODO...


#### LOGGING: `debug` - `info` - `warning` - `error`

TODO...


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

## WHAT IF YOU TRY TO USE THIS CONFIG...

After you created your `dosh.star` file, you can see all available
tasks with the command `dosh` or `dosh help`:

```shell
$ dosh help

Tasks:
  > setup_my_os            place my config files.
  > install_cli_apps       install my favorite apps.
  > update_translations    update django translation files.
    params: langs=str(en|de|tr)
            fuzzy=bool

$ dosh build

$ dosh update_translations -- langs=en,de,tr fuzzy=false
...
```


## QUESTIONS

### CAN I TRUST THIS PROJECT?

No. Don't trust any project. The source code is open, trust yourself
and read the code.


### BUT DO YOU USE THIS PROJECT YOURSELF?

Yes, I use multiple operating systems with different shells, and I'm
too tired to write my scripts in multiple languages.


### WHY DOESN'T DOSH HAVE ANY REMOVE COMMAND?

Because it's too dangerous! I don't use any remove command in my
scripts indeed. If you really need a remove command, you can run it
with `eval`. But remember, contributors of this project don't
guarantee anything.
