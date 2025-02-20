#!/usr/bin/python3
"""
Deletes out-of-date archives created during deployment.
"""

from fabric.api import *

env.hosts = ['35.153.18.12', '52.3.243.162']
env.user = "ubuntu"


def do_clean(number=0):
    """Deletes out-of-date archives"""
    try:
        number = int(number)
    except ValueError:
        return False

    if number < 1:
        number = 1  # Keep at least one archive

    # Delete old archives locally
    local('cd versions && ls -t | tail -n +{} | xargs rm -rf || true'
          .format(number))

    # Delete old archives on remote servers
    r_path = "/data/web_static/releases/"
    run('cd {} && ls -t | tail -n +{} | xargs rm -rf || true'
        .format(r_path, number))
