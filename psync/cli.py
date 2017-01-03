# -*- coding: utf-8 -*-

import click
import subprocess
from psync import psync


@click.command()
def main(args=None):
    """Console script for psync"""
    root = "/Users/lazywei/Code/psync/demo_project"
    conf = psync.load_config(root=root)

    for cmd in psync.cmds_seq(conf):
        subprocess.run(cmd)

    click.echo()
    click.echo("Replace this message by putting your code into "
               "psync.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
