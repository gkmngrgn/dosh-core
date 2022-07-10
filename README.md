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
