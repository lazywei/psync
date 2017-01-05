#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_psync
----------------------------------

Tests for `psync` module.
"""

import os
# from click.testing import CliRunner

from psync import psync
# from psync import cli

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
    assert conf["remote"] == "~/psync"


def test_rsync_cmd():
    conf = psync.load_config(root=PROJ_ROOT)
    cmds = psync.rsync_cmds(conf)

    # rsync -e ssh\
    #       --exclude=GTAGS --exclude=GPATH --exclude=GRTAGS\
    #       -ruaz /Users/lazywei/CMU/Courses/10-605/hw6/6-handout/*\
    #             andrew_linux:~/courses/10-605/hw6/
    assert isinstance(cmds, list)

    assert " ".join(cmds) == "rsync -e ssh -ruaz {} {}:{}".format(
        conf["local"], conf["ssh"]["server"], conf["remote"])


def test_mkdir_cmds():
    conf = psync.load_config(root=PROJ_ROOT)
    cmds = psync.mkdir_cmds(conf)

    assert " ".join(cmds) == "ssh {} mkdir -p {}".format(
        conf["ssh"]["server"], conf["remote"])


def test_cmd_seq():
    conf = psync.load_config(root=PROJ_ROOT)
    cmds = psync.cmds_seq(conf)

    assert isinstance(cmds, list)
    assert len(cmds) == 2
    assert isinstance(cmds[0], list)
    assert isinstance(cmds[1], list)

    assert cmds[0][0] == "ssh"
    assert "mkdir" in cmds[0][-1]
    assert cmds[1][0] == "rsync"


def test_project_root(tmpdir):
    expected_root = tmpdir.mkdir("proj_root")
    expected_root.join(".psync").write("")

    nested_sub = expected_root.mkdir("sub1").mkdir("subsub")
    sub = expected_root.mkdir("sub2")

    none_root = tmpdir.mkdir("no_psync")

    assert psync.project_root(expected_root) == expected_root
    assert psync.project_root(nested_sub) == expected_root
    assert psync.project_root(sub) == expected_root

    assert psync.project_root(none_root) is None


# def test_command_line_interface():
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'psync.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output
