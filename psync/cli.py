# -*- coding: utf-8 -*-

import click
import os
import subprocess
import sys
import time
import yaml

from watchdog.observers import Observer
from . import psync
from . import watcher


if sys.hexversion <= 0x03050000:
    run_shell = subprocess.call
else:
    run_shell = subprocess.run


def get_project_root():
    cwd = os.getcwd()
    root = psync.project_root(start_from=cwd)

    if root is None:
        return False, None
    else:
        return True, root


def ask_for_configs():
    remote_path = click.prompt("Remote path", default="~/remote/path")
    ssh_host = click.prompt("SSH host", default="ssh_host")
    ssh_user = click.prompt("SSH username or enter '-' to skip",
                            default="ssh_user")
    ignores = click.prompt("Files or folders to ignore "
                           "(separated by space)", default=" ")

    if ssh_user == "-":
        ssh_user = None

    if ignores.strip():
        ignores = ignores.split(" ")
    else:
        ignores = []

    return psync.generate_config(ssh_user=ssh_user,
                                 ssh_host=ssh_host,
                                 remote_path=remote_path,
                                 ignores=ignores)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Console script for psync"""
    if ctx.invoked_subcommand is None:
        perform_sync()
    else:
        pass


def perform_sync():
    is_proj, root = get_project_root()

    if not is_proj:
        click.echo("You are not in a project (no .psync found)!")
        cwd = os.getcwd()
        gen_conf = click.prompt(
            "Generate .psync to current directory ({}) [Y/n]?".format(cwd),
            default="Y")

        if gen_conf.lower() == "y":
            click.echo("Config will be generated at {}:".format(cwd))
            click.echo("---")

            conf = ask_for_configs()

            conf_str = yaml.dump(conf, default_flow_style=False)

            click.echo(conf_str)
            click.echo("---")

            with open(os.path.join(cwd, psync.CONFIG_FILE), "w") as f:
                f.write(conf_str)

            click.echo("Project root is now: {}".format(
                psync.project_root(start_from=os.getcwd())))
            click.echo("Run `psync` to perform sync or "
                       "`psync watch` to watch any changes and perform "
                       "sync automatically.")
        else:
            click.echo("Aborted!")
    else:
        conf = psync.load_config(root=root)

        for cmd in psync.cmds_seq(root, conf):
            click.echo("Running: {}".format(cmd[0]))
            run_shell(cmd)

        click.echo("--- Sync Finished ---")


@cli.command()
def watch():
    is_proj, root = get_project_root()

    state = {"dirty": False}

    if not is_proj:
        click.echo("Run psync to generate .psync config file.")
    else:
        click.echo("Start watching {} ...".format(root))
        event_handler = watcher.AnyEventHandler(state)
        observer = Observer()
        observer.schedule(event_handler, root, recursive=True)
        observer.start()
        try:
            while True:
                if state["dirty"]:
                    click.echo("Detect modification. Perform sync.")
                    perform_sync()
                    state["dirty"] = False
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    cli()
