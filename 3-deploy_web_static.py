#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ['35.153.18.12', '52.3.243.162']
env.user = "ubuntu"


def do_pack():
    """Generates a .tgz archive of web_static folder."""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    archive_path = "versions/web_static_{}.tgz".format(time)
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    fname = os.path.splitext(archive_name)[0]
    release_path = "/data/web_static/releases/{}".format(fname)
    tmp_path = "/tmp/{}".format(archive_name)

    try:
        put(archive_path, tmp_path)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(tmp_path, release_path))
        run("rm {}".format(tmp_path))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        
        run("touch {}/0-index.html".format(release_path))
        run("touch {}/my_index.html".format(release_path))

        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
