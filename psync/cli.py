# -*- coding: utf-8 -*-

import click
import subprocess
import os
import yaml
from psync import psync


@click.command()
def main(args=None):
    """Console script for psync"""

    cwd = os.getcwd()
    root = psync.project_root(start_from=cwd)

    if root is None:
        click.echo("You are not in a project (no .psync found)!")
        gen_default_conf = click.prompt(
            "Generate .psync to current directory ({})?".format(cwd),
            default="Y")

        if gen_default_conf.lower() == "y":
            click.echo("Default config is generated at {}:".format(cwd))
            click.echo("---")

            conf = psync.default_config()

            remote_path = click.prompt("Remote path", default=conf["remote"])
            ssh_server = click.prompt("SSH server",
                                      default=conf["ssh"]["server"])

            conf["remote"] = remote_path
            conf["ssh"]["server"] = ssh_server

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
