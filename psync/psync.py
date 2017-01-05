# -*- coding: utf-8 -*-
import yaml
import os

CONFIG_FILE = ".psync"


def project_root(start_from):
    cur_path = start_from
    if os.path.isfile(os.path.join(cur_path, CONFIG_FILE)):
        return cur_path
    elif cur_path == "/":
        return None
    else:
        par_path = os.path.abspath(os.path.join(cur_path, "../"))
        return project_root(par_path)


def load_config(root):
    filepath = os.path.join(root, CONFIG_FILE)

    with open(filepath) as f:
        conf = yaml.load(f.read())

    return conf


def default_config():
    return {
        "remote": "~/remote/path",
        "ssh": {"server": "remote_server"},
    }


def rsync_cmds(local_path, ssh_server, remote_path):
    cmds = ["rsync", "-e", "ssh", "-ruaz",
            "--rsync-path", "mkdir -p {} && rsync".format(remote_path),
            local_path, ssh_server + ":" + remote_path]

    return cmds


def cmds_seq(root, conf):
    return [
        rsync_cmds(root, conf["ssh"]["server"], conf["remote"]),
    ]
