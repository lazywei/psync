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
        "remote:\n  ~/psync\nssh:\n  host: psync_remote_server"
        "\n  username: username"
        "\nignores: []")

    conf = psync.load_config(root=str(proj_root))
    assert isinstance(conf, dict) is True

    assert "local" not in conf
    assert "remote" in conf
    assert "ssh" in conf

    assert isinstance(conf["remote"], str)
    assert isinstance(conf["ssh"], dict)

    assert conf["remote"] == "~/psync"
    assert conf["ssh"]["host"] == "psync_remote_server"
    assert conf["ssh"]["username"] == "username"
    assert len(conf["ignores"]) == 0


def test_rsync_cmd():
    conf = psync.generate_config(ssh_user="ssh_user",
                                 ssh_host="ssh_host",
                                 remote_path="remote_path")
    cmds = psync.rsync_cmds("fake/local/path", conf)

    assert isinstance(cmds, list)

    assert (" ".join(cmds) ==
            "rsync -e ssh -ruaz --rsync-path mkdir -p {} && rsync {} {}".
            format(conf["remote"], "fake/local/path",
                   psync.ssh_path(conf["ssh"], conf["remote"])))

    ig_conf = psync.generate_config(ssh_user="ssh_user",
                                    ssh_host="ssh_host",
                                    remote_path="remote_path",
                                    ignores=["folderA", "fileB"])

    ignores_cmds = psync.rsync_cmds("fake/local/path", ig_conf)
    assert "--exclude" in ignores_cmds
    assert "folderA" in ignores_cmds
    assert "fileB" in ignores_cmds


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


def test_generate_conf():
    conf = psync.generate_config(ssh_user="ssh_user",
                                 ssh_host="ssh_host",
                                 remote_path="remote_path")

    assert conf["ssh"]["host"] == "ssh_host"
    assert conf["ssh"]["username"] == "ssh_user"
    assert conf["remote"] == "remote_path"
    assert len(conf["ignores"]) == 0

    nouser_conf = psync.generate_config(ssh_user=None,
                                        ssh_host="ssh_host",
                                        remote_path="remote_path")

    assert nouser_conf["ssh"]["host"] == "ssh_host"
    assert nouser_conf["ssh"]["username"] is None
    assert nouser_conf["remote"] == "remote_path"

    ignores_conf = psync.generate_config(ssh_user=None,
                                         ssh_host="ssh_host",
                                         remote_path="remote_path",
                                         ignores=["folderA", "fileB"])

    assert ignores_conf["ignores"] == ["folderA", "fileB"]


def test_ssh_path():
    conf = psync.generate_config(ssh_user="ssh_user",
                                 ssh_host="ssh_host",
                                 remote_path="remote_path")
    ssh_path = psync.ssh_path(conf["ssh"], conf["remote"])

    assert ssh_path == "{}@{}:{}".format(
        conf["ssh"]["username"], conf["ssh"]["host"],
        conf["remote"])

    conf["ssh"]["username"] = None

    nouser_ssh_path = psync.ssh_path(conf["ssh"], conf["remote"])
    assert nouser_ssh_path == "{}:{}".format(
        conf["ssh"]["host"], conf["remote"])


# def test_command_line_interface():
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'psync.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output
