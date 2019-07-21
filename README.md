# DOSH [IN PROGRESS]

Dosh is a zero-dependency way to standardize all your development-related commands. Consider you have some projects in different languages or different technical stacks.

It's possible to generate a shell script using dosh if you don't want to install anything. Currently, it supports only BASH and PowerShell.

```
$ dosh
Available Environments
  - DEV (default)
  - PROD
  - TEST

Available Commands
  > build                Build or rebuild services
  > deploy               Deploy the project to the servers
  > initdb
  > shell
  > start                Create and start containers

$ ENV=PROD dosh deploy
Environment: PROD
    Command: # TODO: fill here
...

$ dosh build
Environment: DEV
    Command: docker-compose -p dosh -f docker-compose.yml -f docker-compose.dev.yml build
...

$ dosh start
Environment: DEV
    Command: docker-compose -p dosh -f docker-compose.yml -f docker-compose.dev.yml start
```

## Commands

- MKDIR
- PRINT
- RUN

## Build

```shell
dosh build
dosh start dosh-cli
```

## Test

```shell
dosh runtests
dosh coverage
```

# License
See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

# To Do
[ ] Parse commands and write unit tests for each command.
