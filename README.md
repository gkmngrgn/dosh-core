# DOSH - shell-independent task manager

Create your `dosh.lua` file in the project folder -or anywhere- and define your tasks,
aliases, environments. Dosh will work like a CLI app reading your config file.

<img src="./files/dosh-logo.png" width=200 />


## ENVIRONMENT VARIABLES

#### HELP OUTPUT

Help outputs consist of three parts: description, tasks, epilog. The tasks are generated
reading your config but you can edit the other parts defining these variables:

- `HELP_DESCRIPTION`
- `HELP_EPILOG`

If you want to delete the description or epilog, define it as `nil`.


#### OPERATING SYSTEM TYPE CHECKING

OS type variables to detect your current operating system. All variables return `true`
or `false`. You can find many examples of use of these variables in the documentation.

- `env.IS_LINUX`
- `env.IS_MACOS`
- `env.IS_WINDOWS`


#### SHELL TYPE CHECKING

Your current shell. All these variables return `true` or `false`. It's useful if you use
shell-specific package like `ohmyzsh`.

- `IS_BASH`
- `IS_PWSH`
- `IS_ZSH`


#### DOSH-SPECIFIC ENVIRONMENTS

Consider you have some tasks that help you to test the project on your local and you
want to restrict the task to prevent running it on the server by mistake. So the method
`cmd.add_task` has an `environments` parameter and you can set your environment name for
each target.

- `DOSH_ENV` (define it on your `~/.profile` file or CI/CD service)

_Check out the file [`dosh_environments.lua`](./examples/dosh_environments.lua) for
example usage._


## FUNCTIONS

#### GENERAL PURPOSE

The main purpose of dosh to write one script that works on multiple operating systems
and shells. But it has to have a limit and it's nonsense to define functions for each
command. So if you want to run a cli app (like `exa`, `bat`, `helix`, etc.), then you
can use `run` for it.

_Check out the file [`dosh_greet.lua`](./examples/dosh_greet.lua) for example usage._


#### FILE SYSTEM OPERATIONS

There are some ready-made functions both to keep the code readable and to make it work
the same in every operating system. You know Windows prefers backslash as a path
separator. This code will work on all operating systems.

_Check out the file [`dosh_config.lua`](./examples/dosh_config.lua) for example usage._


#### PACKAGE MANAGERS

There are many package managers and I'm not sure if we need to implement all of
them. But at least I'm using these three of them mostly:

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

You can manage the command outputs by defining the verbosity level. It's still possible
to use `print`, but if you want to hide the command outputs completely or print them by
the verbosity level, you have to use these logging functions:

- `debug`
- `info`
- `warning`
- `error`

For more information about the verbosity parameter of dosh, type `dosh help`.

_Check out the file [`dosh_greet.lua`](./examples/dosh_greet.lua) for example usage._


## ANATOMY OF `dosh.lua`

```lua
local name = "there"                         -- you can use all features of Lua programming language.

local function hello(there)                  -- even you can define your custom functions.
    there = there or name
    local message = "Hello, " .. there .. "!"
    cmd.run("osascript -e 'display notification \"" .. message .. "\" with title \"Hi!\"'")
end

cmd.add_task{                                -- cmd comes from dosh.
   name="hello",                             -- task name, or subcommand for your cli.
   description="say hello",                  -- task description for the help output.
   required_commands={"osascript"},          -- check if the programs exist before running the task.
   environments={"development", "staging"},  -- DOSH_ENV variable should be either development or staging to run this task.
   command=hello                             -- run hello function with its parameters when the task ran.
}
```

When you ran this command on MacOS, you will get a notification:

```shell
$ dosh help
dosh - shell-independent task manager

Tasks:
  > hello                say hello

Dosh commands:
  > help                 print this output
  > init                 initialize a new config in current working directory

  -c, --config PATH      specify config path (default: dosh.lua)
  -v|vv|vvv, --verbose   increase the verbosity of messages:
                         1 - default, 2 - detailed, 3 - debug

$ DOSH_ENV="development" dosh hello lua
DOSH => [RUN] osascript -e 'display notification "Hello, lua!" with title "Hi!"'
```

Take a look at the [`examples`](./examples) folder to find ready-in-use config files.


## QUESTIONS

### CAN I TRUST THIS PROJECT?

No. Don't trust any project. The source code is open, trust yourself and read the code.


### BUT DO YOU USE THIS PROJECT YOURSELF?

Yes, I use multiple operating systems with different shells, and I'm too tired to write
my scripts in multiple languages. This is why I created this project.


### WHY DOESN'T DOSH HAVE ANY REMOVE COMMAND?

Because it's too dangerous! I don't use any remove command in my scripts indeed. If you
really need a remove command, you can run it with `run`. But remember, contributors of
this project don't guarantee anything.


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
