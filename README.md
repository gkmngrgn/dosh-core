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

    if SHELL == "zsh":
        if not exists(home_dir(".oh-my-zsh")):
            url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
            eval(url, type="shell", fetch=True)

        if exists("conda", type="command"):
            eval("conda init zsh")

    tpm_folder = home_dir(".tmux/plugins/tpm")
    if exists(tpm_folder):
        print("update tpm repository...")
        sync(tpm_folder)
    else:
        url = "https://github.com/tmux-plugins/tpm"
        clone(url, directory=tpm_folder)

    if not exists("nvm", type="command"):
        url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh"
        eval(url, type="shell", fetch=True)


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
