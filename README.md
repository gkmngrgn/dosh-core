# DOSH

Shell-independent command manager. Create your bazel scripts in
`./.dosh/` folder file and define your custom commands, alias,
environments. Dosh will generate a script for your favorite shell.


    ┌──────────────────────────────────────────────────────────────┐
    │  DOSH SCRIPTS                                                │
    │  Folder: /.dosh/                                             │
    ├──────────────────────────────────────────────────────────────┤
    │  ┌───────────────────┐          ┌─────────────────────────┐  │
    │  │  BUILD            ◄──────┬───┤  COMMON FUNCTIONS &     │  │
    │  │  Run: dosh build  │      │   │  ENVIRONMENT VARIABLES  │  │
    │  │  File: build.bzl  │      │   │  File: dosh.bzl         │  │
    │  └───────────────────┘      │   └─────────────────────────┘  │
    │  ┌──────────────────────┐   │                                │
    │  │  SHELL (for Docker)  ◄───┘                                │
    │  │  Run: dosh shell     │                                    │
    │  │  File: shell.bzl     │                                    │
    │  └──────────────────────┘                                    │
    └──────────────────────────────────────────────────────────────┘


## GENERATION OVERVIEW

1. Write your commands in Bazel.
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
    ...

    $ dosh update_translations -- langs=en,de,tr fuzzy=false
    ...


## PRE-DEFINED FUNCTIONS

- [ ] eval
- [ ] mkdir
- [ ] copy


## TODO

- [-] First starlark implementation.
- [ ] Read commands from a JSON file.
- [ ] Use MessagePack instead of JSON for (de)serialization process.
- [ ] Add `help.bzl` with initialize. So devs can use that file as a
      sample.
- [ ] Generate BASH script from TOML.
- [ ] Generate PWSH script from .
