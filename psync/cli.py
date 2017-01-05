# -*- coding: utf-8 -*-

import click
import subprocess
import os
from psync import psync


@click.command()
def main(args=None):
    """Console script for psync"""

    root = psync.project_root(start_from=os.getcwd())

    if root is None:
        click.echo("You are not in a project (no .psync found)!")
    else:
        conf = psync.load_config(root=root)

        for cmd in psync.cmds_seq(conf):
            click.echo("Running:\n  {}".format(" ".join(cmd)))
            subprocess.run(cmd)

        click.echo("--- Sync Finished ---")


if __name__ == "__main__":
    main()
