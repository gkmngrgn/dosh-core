# DOSH

Shell-independent task manager. Create your `dosh.lua` file in the
project folder and define your tasks, aliases, environments. Dosh will
work like a CLI app reading your config file.


## ENVIRONMENT VARIABLES

#### HELP OUTPUT

Help outputs consist of three parts: description, tasks, epilog. The
tasks are generated reading your config but you can edit the other
parts defining these variables:

- `HELP_DESCRIPTION`
- `HELP_EPILOG`

If you want to delete the description or epilog, define it as `nil`.


#### OPERATING SYSTEM TYPE CHECKING

OS type variables to detect your current operating system. All
variables return `true` or `false`. You can find many examples of use
of these variables in the documentation.

- `IS_LINUX`
- `IS_MACOS`
- `IS_WINDOWS`


#### SHELL TYPE CHECKING

Your current shell. All these variables return `true` or `false`. It's
useful if you use shell-specific package like `ohmyzsh`.

- `IS_BASH`
- `IS_PWSH`
- `IS_ZSH`


#### DOSH-SPECIFIC ENVIRONMENTS

Consider you have some tasks that help you to test the project on your
local and you want to restrict the task to prevent running it on the
server by mistake. So the method `cmd.add_task` has an `environments`
parameter and you can set your environment name for each target.

- `DOSH_ENV` (define it on your `~/.profile` file or CI/CD service)

_Check out the file [`dosh_environments.lua`](./examples/dosh_environments.lua) for example usage._


## FUNCTIONS

#### GENERAL PURPOSE

The main purpose of dosh to write one script that works on multiple
operating systems and shells. But it has to have a limit and it's
nonsense to define functions for each command. So if you want to run a
cli app (like `exa`, `bat`, `helix`, etc.), then you can use `run` for
it.

_Check out the file [`dosh_greet.lua`](./examples/dosh_greet.lua) for example usage._


#### FILE SYSTEM OPERATIONS

There are some ready-made functions both to keep the code readable and
to make it work the same in every operating system. You know Windows
prefers backslash as a path separator. This code will work on all
operating systems.

_Check out the file [`dosh_config.lua`](./examples/dosh_config.lua) for example usage._


#### PACKAGE MANAGERS

There are many package managers and I'm not sure if we need to
implement all of them. But at least I'm using these three of them
mostly:

- `brew_install` (for MacOS and Linux)
  - `packages`: list of strings, required.
  - `cask`: boolean, default is `false`.
  - `taps`: list of strings, optional.

- `apt_install` (for Debian based Linux distros)
  - `packages`: list of strings, required.

- `winget_install` (for Windows)
  - `packages`: list of strings, required.

_Check out the file [`dosh_config.lua`](./examples/dosh_config.lua) for example usage._


#### FILE, FOLDER, COMMAND EXISTENCY: `exists`, `exists_command`

TODO...


#### LOGGING

You can manage the command outputs by defining the verbosity
level. It's still possible to use `print`, but if you want to hide the
command outputs completely or print them by the verbosity level, you
have to use these logging functions:

- `debug`
- `info`
- `warning`
- `error`

For more information about the verbosity parameter of dosh, type `dosh help`.

_Check out the file [`dosh_greet.lua`](./examples/dosh_greet.lua) for example usage._


## EXAMPLE CONFIGURATION

```lua
local config_dir = "~/.config"

cmd.add_task{
   name="config_os",
   description="copy my configuration files and replace",
   command=function()
      -- copy config files.
      cmd.copy("./config/*", config_dir)
      cmd.copy("./home/.*", "~")

      -- zsh specific settings
      if env.IS_ZSH then
         if not cmd.exists("~/.oh-my-zsh") then
            cmd.run_url("https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh")
         end

         if cmd.exists_command("conda") then
            cmd.run("conda init zsh")
         end
      end

      -- tmux
      cmd.clone{
         url="https://github.com/tmux-plugins/tpm",
         destination="~/.tmux/plugins/tmp",
         fetch=true,
      }
   end
}

cmd.add_task{
   name="install_cli_apps",
   description="install my favourite apps",
   command=function ()
      if env.IS_WINDOWNS then
         local packages = {"Git.Git", "VSCodium.VSCodium", "Discord.Discord", "Valve.Steam"}
         cmd.winget_install(packages)
      elseif env.IS_MACOS then
         local packages = {
            "MisterTea/et/et", "bat", "clojure", "cmake", "deno", "exa", "exercism", "fd",
            "git-delta", "git-lfs", "golang", "helix", "htop", "hugo", "jq", "llvm",
            "multimarkdown", "openssl", "pass", "pre-commit", "ripgrep", "rustup-init",
            "rust-analyzer", "shellcheck", "tmux", "font-ibm-plex", "miktex-console", "miniconda"
         }
         local taps = {"helix-editor/helix"}
         cmd.brew_install{packages, cask=true, taps=taps}
      elseif env.IS_LINUX then
         local packages = {"git", "ripgrep"}
         cmd.apt_install(packages)
      end

      if not cmd.IS_WINDOWS and not cmd.exists_command("nvm") then
         cmd.run_url("https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh")
      end
   end
}
```


## WHAT IF YOU TRY TO USE THIS CONFIG...

After you created your `dosh.lua` file, you can see all available
tasks with the command `dosh help`:

```shell
$ dosh help  # or just dosh
dosh - shell-independent command manager

Tasks:
  > config_os          copy my configuration files and replace
  > install_cli_apps   install my favourite apps
  > change_theme       sync your editor theme with system

Dosh commands:
  > help                 print this output
  > init                 initialize a new config in current working directory

  -c, --config PATH      specify config path (default: dosh.lua)
  -v|vv|vvv, --verbose   increase the verbosity of messages:
                         1 - default, 2 - detailed, 3 - debug
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
with `run`. But remember, contributors of this project don't
guarantee anything.


## CONTRIBUTION

Install these development dependencies manually:

- [poetry](https://python-poetry.org/)
- [poethepoet](https://github.com/nat-n/poethepoet)
- [pre-commit](https://pre-commit.com/)

```shell
$ poetry install
$ poetry run dosh   # run dosh without instaling.
$ poetry poe lint   # run pre-commit hooks manually.
$ poetry poe test   # run unit tests.
$ poetry poe build  # build and generate self-executable file.
```
