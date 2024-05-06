#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """ generates a .tgz archive """
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("versions"):
        local('mkdir versions')
    arch_path = 'versions/web_static_{}.tgz'.format(time)
    archive = local('tar -cvzf {} web_static'.format(arch_path))
    if archive.return_code != 0:
        return None
    else:
        return arch_path
