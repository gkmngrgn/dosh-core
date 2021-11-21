# DOSH

Shell-independent command manager. Create your bazel scripts in
`./.dosh/` folder file and define your custom commands, alias,
environments. Dosh will generate a script for your favorite shell.


    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │  DOSH SCRIPTS                                                │
    │                                                              │
    │  Folder: /.dosh/                                             │
    │                                                              │
    ├──────────────────────────────────────────────────────────────┤
    │                                                              │
    │  ┌───────────────────┐          ┌─────────────────────────┐  │
    │  │                   │          │                         │  │
    │  │  BUILD            ◄──────┬───┤  COMMON FUNCTIONS &     │  │
    │  │                   │      │   │                         │  │
    │  │  Run: dosh build  │      │   │  ENVIRONMENT VARIABLES  │  │
    │  │                   │      │   │                         │  │
    │  │  File: build.bzl  │      │   │  File: dosh.bzl         │  │
    │  │                   │      │   │                         │  │
    │  └───────────────────┘      │   └─────────────────────────┘  │
    │                             │                                │
    │  ┌──────────────────────┐   │                                │
    │  │                      │   │                                │
    │  │  SHELL (for Docker)  ◄───┘                                │
    │  │                      │                                    │
    │  │  Run: dosh shell     │                                    │
    │  │                      │                                    │
    │  │  File: shell.bzl     │                                    │
    │  │                      │                                    │
    │  └──────────────────────┘                                    │
    │                                                              │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘


After you created your .bzl scripts, you can see all available
commands with `--help` or `-h`:

    $ dosh --help

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
