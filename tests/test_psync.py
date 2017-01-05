#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_psync
----------------------------------

Tests for `psync` module.
"""

# from click.testing import CliRunner

from psync import psync
# from psync import cli


def test_load_config(tmpdir):
    proj_root = tmpdir.mkdir("proj_root")
    proj_root.join(".psync").write(
        "remote:\n  ~/psync\nssh:\n  server: psync_remote_server")

    conf = psync.load_config(root=str(proj_root))
    assert isinstance(conf, dict) is True

    assert "local" not in conf
    assert "remote" in conf
    assert "ssh" in conf

    assert isinstance(conf["remote"], str)
    assert isinstance(conf["ssh"], dict)
    assert "server" in conf["ssh"]

    assert conf["remote"] == "~/psync"
    assert conf["ssh"]["server"] == "psync_remote_server"


def test_rsync_cmd():
    conf = psync.default_config()
    cmds = psync.rsync_cmds("fake/local/path",
                            conf["ssh"]["server"], conf["remote"])

    # rsync -e ssh\
    #       --exclude=GTAGS --exclude=GPATH --exclude=GRTAGS\
    #       -ruaz /Users/lazywei/CMU/Courses/10-605/hw6/6-handout/*\
    #             andrew_linux:~/courses/10-605/hw6/
    assert isinstance(cmds, list)

    assert (" ".join(cmds) ==
            "rsync -e ssh -ruaz --rsync-path mkdir -p {} && rsync {} {}:{}".
            format(conf["remote"], "fake/local/path",
                   conf["ssh"]["server"], conf["remote"]))


def test_project_root(tmpdir):
    expected_root = tmpdir.mkdir("proj_root")
    expected_root.join(".psync").write("")

    nested_sub = expected_root.mkdir("sub1").mkdir("subsub")
    sub = expected_root.mkdir("sub2")

    none_root = tmpdir.mkdir("no_psync")

    assert psync.project_root(str(expected_root)) == expected_root
    assert psync.project_root(str(nested_sub)) == expected_root
    assert psync.project_root(str(sub)) == expected_root

    assert psync.project_root(str(none_root)) is None


def test_default_conf():
    default_conf = psync.default_config()

    assert "ssh" in default_conf
    assert "server" in default_conf["ssh"]
    assert "remote" in default_conf

# def test_command_line_interface():
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'psync.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output
