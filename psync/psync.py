# -*- coding: utf-8 -*-
import yaml
import os

CONFIG_FILE = ".psync"


def load_config(root):
    filepath = os.path.join(root, CONFIG_FILE)

    with open(filepath) as f:
        conf = yaml.load(f.read())

    conf["local"] = os.path.normpath(os.path.join(root, conf["local"]))
    # conf = {
    #     "local": "/Users/lazywei/Code/psync/demo_project",
    #     "remote": "~/psync/demo_project",
    #     "ssh": {
    #         "server": "aws_playground",
    #     },
    # }

    return conf


def mkdir_cmds(conf):
    return ["ssh", conf["ssh"]["server"],
            "mkdir -p {}".format(conf["remote"])]


def rsync_cmds(conf):
    cmds = ["rsync", "-e", "ssh", "-ruaz",
            conf["local"], conf["ssh"]["server"] + ":" + conf["remote"]]

    return cmds


def cmds_seq(conf):
    return [
        mkdir_cmds(conf),
        rsync_cmds(conf),
    ]
