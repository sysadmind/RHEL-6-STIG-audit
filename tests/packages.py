import yum
import os
import ConfigParser

from utils import console


def run_tests():
    yb = yum.YumBase()
    pass

    # Verify GPG check
    # RHEL-06-000013
    config = ConfigParser.RawConfigParser()
    config.read("/etc/yum.conf")
    gpg_check = config.getint("main", "gpgcheck")
    if gpg_check == 1:
        console.ok("GPG checking is enabled in yum")

    else:
        console.error("GPG checking is disabled in yum")

    # Verify GPG check for all repos
    # RHEL-06-000015
    repo_files = os.listdir("/etc/yum.repos.d/")
    for repo_file in repo_files:

        repo_file = "/etc/yum.repos.d/" + repo_file
        repo_config = ConfigParser.RawConfigParser()
        repo_config.read(repo_file)

        for section in repo_config.sections():

            gpg_check = repo_config.getint(section, 'gpgcheck')
            if gpg_check != 1:
                console.error("GPG checking is disabled in yum repo: %s" % section)

