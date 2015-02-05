import pwd
import os

from utils import console


def run_tests():

    # Check for Rsh files
    # RHEL-06-000019
    if os.path.isfile("/etc/hosts.equiv"):
        console.error("/etc/hosts.equiv file exists!")
    users = pwd.getpwall()
    for user in users:
        if os.path.isfile(user.pw_dir + "/.rhosts"):
            console.error("%s exists!" % (user.pw_dir + "/.rhosts"))

    # Check for password hashes in the /etc/passed file
    #  RHEL-06-000031
    for user in users:
        if user.pw_passwd != 'x':
            console.error("User %s has a hashed password in /etc/passwd" % user.pw_name)

    # Check for users with a UID of 0 other than root
    #  RHEL-06-000032
    for user in users:
        if user.pw_uid == 0:
            if user.pw_name != 'root':
                console.error("User %s has a UID of 0" % user.pw_name)
