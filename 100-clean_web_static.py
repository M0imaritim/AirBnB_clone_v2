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
        number = 1  # If number is 0, keep only 1 archive

    # Deleting old archives locally
    local('cd versions && ls -t | tail -n +{} | xargs rm -rf || true'
          .format(number + 1))

    # Deleting old archives remotely
    r_path = "/data/web_static/releases/"
    run('cd {} && ls -t | tail -n +{} | xargs rm -rf || true'
        .format(r_path, number + 1))
