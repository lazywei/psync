#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_psync
----------------------------------

Tests for `psync` module.
"""

from click.testing import CliRunner

from psync import psync
from psync import cli

PROJ_ROOT = "/Users/lazywei/Code/psync/demo_project"


def test_load_config():
    conf = psync.load_config(root=PROJ_ROOT)
    assert isinstance(conf, dict) is True

    conf_keys = conf.keys()
    assert "local" in conf_keys
    assert "remote" in conf_keys
    assert "ssh" in conf_keys

    assert isinstance(conf["local"], str)
    assert isinstance(conf["remote"], str)
    assert isinstance(conf["ssh"], dict)
    assert "server" in conf["ssh"].keys()

    assert conf["local"] == PROJ_ROOT
    assert conf["remote"] == "~/psync/demo_project"


def test_rsync_cmd():
    conf = psync.load_config(root=PROJ_ROOT)
    cmd = psync.rsync_cmd(conf)

    # rsync -e ssh\
    #       --exclude=GTAGS --exclude=GPATH --exclude=GRTAGS\
    #       -ruaz /Users/lazywei/CMU/Courses/10-605/hw6/6-handout/*\
    #             andrew_linux:~/courses/10-605/hw6/
    assert cmd == "rsync -e ssh -ruaz {} {}:{}".format(conf["local"],
                                                       conf["ssh"]["server"],
                                                       conf["remote"])


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'psync.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
