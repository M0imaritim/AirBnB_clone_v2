#!/usr/bin/python3
""" deletes out-of-date archives """
from fabric.api import *


env.hosts = ['54.145.240.184', '54.89.109.0']
env.user = "ubuntu"


def do_clean(number=0):
    """Deletes out-of-date archives"""
    try:
        number = int(number)
    except ValueError:
        return False

    if number < 0:
        return False
    elif number == 0 or number == 1:
        number = 1

    with lcd("versions"):
        archives = sorted(os.listdir("."), reverse=True)

        # Delete unnecessary archives
        for archive in archives[number:]:
            local("rm -f {}".format(archive))

        releases_path = "/data/web_static/releases/"
        with lcd(releases_path):
            archives = run("ls -1t").split()

            # Delete unnecessary archives
            for archive in archives[number:]:
                run("rm -rf {}".format(os.path.join(releases_path, archive)))

        return True
