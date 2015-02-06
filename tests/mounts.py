import os

from utils import console


mount_points = [
    "/tmp",             # RHEL-06-000001
    "/var",             # RHEL-06-000002
    "/var/log",         # RHEL-06-000003
    "/var/log/audit",   # RHEL-06-000004
    "/home",            # RHEL-06-000007
]


def run_tests():
    console.heading("System Mounts")

    for mount_point in mount_points:

        if os.path.ismount(mount_point):
            console.ok("%s is a mount point" % mount_point)

        else:
            console.error("%s is not a mount point" % mount_point)
