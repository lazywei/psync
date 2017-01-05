# -*- coding: utf-8 -*-

import click
import subprocess
import os
import yaml
from psync import psync


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


@click.command()
def main(args=None):
    """Console script for psync"""

    cwd = os.getcwd()
    root = psync.project_root(start_from=cwd)

    if root is None:
        click.echo("You are not in a project (no .psync found)!")
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
        else:
            click.echo("Aborted!")
    else:
        conf = psync.load_config(root=root)

        for cmd in psync.cmds_seq(root, conf):
            click.echo("Running:\n  {}".format(" ".join(cmd)))
            subprocess.run(cmd)

        click.echo("--- Sync Finished ---")


if __name__ == "__main__":
    main()
