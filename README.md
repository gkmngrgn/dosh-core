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


## EXAMPLE CONFIGURATION

```python
# dosh.star

CONFIG_DIR = home_dir(".config")
BIN_DIR = home_dir(".local/bin")


def cmd_install():
    """Install config files."""

    copy("./config/*", CONFIG_DIR)
    copy("./home/.*", HOME)

    if IS_ZSH:
        if not exists(home_dir(".oh-my-zsh")):
            eval_url("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")

        if exists_command("conda"):
            eval("conda init zsh")

    clone(
        url="https://github.com/tmux-plugins/tpm",
        folder=home_dir(".tmux/plugins/tpm"),
        sync=True,
    )

    if not exists_command("nvm"):
        eval_url("https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh")


def cmd_install_cli_apps():
    """Install required packages."""

    if IS_WINDOWS:
        winget_install("git", "git-delta", "git-lfs", "golang", "helix", "hugo", "ripgrep")
        return

    if IS_MACOS:
        brew_install("font-ibm-plex", "miktex-console", "miniconda")

    brew_tap("helix-editor/helix")

    brew_install(
        "MisterTea/et/et", "bat", "clojure", "cmake", "deno", "exa", "exercism", "fd",
        "git-delta", "git-lfs", "golang", "helix", "htop", "hugo", "jq", "llvm",
        "multimarkdown", "openssl", "pass", "pre-commit", "ripgrep", "rustup-init",
        "rust-analyzer", "shellcheck", "tmux")
```


## ENVIRONMENT VARIABLES

- `HOME`

- `OSTYPE`

- `SHELL`


## FUNCTIONS

- `brew_install`

- `copy`

- `env`

- `eval`

- `exists, type={file_or_directory(default),command}`

- `home_dir`

- `print`

- `sync`


## QUESTIONS

### WHY DOESN'T DOSH HAVE ANY REMOVE COMMAND?

Because it's too dangerous! Even the authors and contributors of this
project don't guarantee anything. If you really need a remove command,
you can run it with `eval`.
