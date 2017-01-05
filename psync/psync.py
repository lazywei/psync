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


def generate_config(ssh_user, ssh_host, remote_path):
    if ssh_user == "-":
        ssh_user = None

    return {
        "remote": remote_path,
        "ssh": {
            "username": ssh_user,
            "host": ssh_host,
        },
    }


def ssh_path(ssh_conf, remote_path):
    username = ssh_conf["username"]
    ssh_host = ssh_conf["host"]

    if username is None:
        return "{}:{}".format(ssh_host, remote_path)
    else:
        return "{}@{}:{}".format(username, ssh_host, remote_path)


def rsync_cmds(local_path, ssh_conf, remote_path):
    cmds = ["rsync", "-e", "ssh", "-ruaz",
            "--rsync-path", "mkdir -p {} && rsync".format(remote_path),
            local_path, ssh_path(ssh_conf, remote_path)]

    return cmds


def cmds_seq(root, conf):
    return [
        rsync_cmds(root, conf["ssh"], conf["remote"]),
    ]
