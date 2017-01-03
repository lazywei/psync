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


def rsync_cmd(conf):
    cmd = "rsync -e ssh -ruaz {} {}:{}".format(
        conf["local"], conf["ssh"]["server"], conf["remote"])

    return cmd
