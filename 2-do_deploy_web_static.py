#!/usr/bin/python3
"""distributes an archive to your web servers"""
from datetime import datetime
from fabric.api import *
import os
import shlex


env.hosts = ['54.145.240.184', '54.89.109.0']
env.user = "ubuntu"


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if os.path.exists(archive_path):
        native = archive_path.replace('/', ' ')
        native = shlex.split(native)
        native = native[-1]

        fname = native.replace('.', ' ')
        fname = shlex.split(fname)
        fname = fname[0]

        f_path = "/data/web_static/releases/{}/".format(fname)
        t_path = "/tmp/{}".format(native)

        put(archive_path, t_path)
        run("mkdir -p {}".format(f_path))
        run("tar -xzf {} -C {}".format(t_path, f_path))
        run("rm {}".format(t_path))
        run("mv -f {}web_static/* {}".format(f_path, f_path))
        run("rm -rf {}web_static".format(f_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(f_path))
        return True
    return False
