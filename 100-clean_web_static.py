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
    elif number == 0:
        number = 2
    else:
        number += 1

   local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
   r_path = "/data/web_static/releases/"
   run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(r_path, number))
