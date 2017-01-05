Project Sync
=======================

A simple tool for synchronizing local project (files) to remote server.

## Installation

```
$ pip install psync
```


## Usage


1. Run `psync` under project root to generate initial config file (`.psync`).
    ```
    $ cd ~/Code/demo_project
    $ psync
    ```
    It will generate the config interactively:

    ```
    You are not in a project (no .psync found)!
    Generate .psync to current directory (/Users/lazywei/Code/demo_project) [Y/n]? [Y]: Y
    Config will be generated at /Users/lazywei/Code/demo_project:
    ---
    Remote path [~/remote/path]: ~/remote/path
    SSH host [ssh_host]: aws_playground
    SSH username or enter '-' to skip [ssh_user]: -
    Files or folders to ignore (separated by space) [ ]: .git .psync
    ignores:
    - .git
    - .psync
    remote: ~/remote/path
    ssh:
      host: aws_playground
      username: null
    
    ---
    Project root is now: /Users/lazywei/Code/demo_project
    ```

2. Run `psync` under any nested subfolders of the project root to sync the project.
    ```
    $ psync
    Running:
      rsync -e ssh -ruaz --exclude .git --exclude .psync --rsync-path mkdir -p ~/remote/path && rsync /Users/lazywei/Code/demo_project aws_playground:~/remote/path
    --- Sync Finished ---
    
    $ ssh aws_playground "ls -a ~/remote/path/demo_project"
    .      ..     README
    ```

### Usage Demo

[![Usage Demo](https://asciinema.org/a/98202.png)](https://asciinema.org/a/98202)

### Config Options

The config (`.psync`) is a YAML file. You can edit it after initial generating.

- `ignores`: an array contains all the files for folders to exclude by `rsync`
- `ssh`:
  - `host`: SSH Host
  - `username`: SSH username, `null` to ignore this (for example, when you set this in `~/.ssh/config` already)
- `remote`: where to sync on remote server

## Contributions

This project is currently WIP stage, so discussion, bug report and PR are really welcome :wink:.

## License

psync is available under the MIT license. See the LICENSE file for more info.
