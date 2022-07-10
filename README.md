# DOSH

Shell-independent command manager. Create your bazel scripts in
`./.dosh/` folder file and define your custom commands, alias,
environments. Dosh will generate a script for your favorite shell.


## GENERATION OVERVIEW

1. Write your commands in Starlark.
2. DOSH generates a JSON file for handling all commands.
3. DOSH can generate also a BASH or PWSH script.


## USAGE

After you created your .bzl scripts, you can see all available
commands with `help`:

    $ dosh help

    Available commands:
      > build             build your project.
      > shell             log in to docker shell.


    $ dosh build

    $ dosh update_translations -- langs=en,de,tr fuzzy=false
    ...

## EXAMPLE CONFIGURATION

```python
CONFIG_DIR = home_dir(".config")
BIN_DIR = home_dir(".local/bin")


def cmd_install():
    """Install config files."""

    copy("./config/*", CONFIG_DIR)
    copy("./home/.*", HOME)

    if SHELL == "zsh":
        if not exists(home_dir(".oh-my-zsh")):
            eval("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh", type="shell", fetch=True)

        if exists("conda", type="command"):
            eval("conda init zsh")

    tpm_folder = home_dir(".tmux/plugins/tpm")
    if not exists(tpm_folder):
        clone("https://github.com/tmux-plugins/tpm", directory=tpm_folder)
    else:
        print("update tpm repository...")
        sync(tpm_folder)

    if not exists("nvm", type="command"):
        eval("https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh", type="shell", fetch=True)


def cmd_install_cli_apps():
    """Install required packages."""

    brew_install("helix", tap="helix-editor/helix")

    brew_install([
        "MisterTea/et/et", "bat", "clojure", "cmake", "deno", "exa", "exercism", "fd",
        "git-delta", "git-lfs", "golang", "htop", "hugo", "jq", "llvm",
        "multimarkdown", "openssl", "pass", "pre-commit", "ripgrep", "rustup-init",
        "rust-analyzer", "shellcheck", "tmux"])

    if OSTYPE == "darwin":
        brew_install(["font-ibm-plex", "miktex-console", "miniconda"])
```


## ENVIRONMENT VARIABLES

### `HOME`

### `OSTYPE`

### `SHELL`


## FUNCTIONS

### `brew_install`

### `copy`

### `eval`

### `exists`

Parameters:

- `file_or_directory` (default)
- `command`

### `home_dir`

### `print`

### `sync`
