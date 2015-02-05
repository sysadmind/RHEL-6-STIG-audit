import os
import stat

from utils import console, parsing


def isgroupreadable(stats):
    return bool(stats.st_mode & stat.S_IRGRP)


def is_group_writable(stats):
    return bool(stats.st_mode & stat.S_IWGRP)


def is_world_writable(stats):
    return bool(stats.st_mode & stat.S_IWOTH)


def get_owner_permissions_int(stats):
    permissions = oct(stats.st_mode & stat.S_IRWXU)
    if permissions == oct(0):
        return 0
    else:
        return int(permissions[1])


def get_group_permissions_int(stats):
    permissions = oct(stats.st_mode & stat.S_IRWXG)
    if permissions == oct(0):
        return 0
    else:
        return int(permissions[1])


def get_world_permissions_int(stats):
    permissions = oct(stats.st_mode & stat.S_IRWXO)
    if permissions == oct(0):
        return 0
    else:
        return int(permissions[1])


def shadow_file_tests():
    # RHEL-06-000033
    shadow_file = os.stat("/etc/shadow")
    if shadow_file.st_uid != 0:
        console.error("/etc/shadow is not owned by root!")

    # RHEL-06-000034
    if shadow_file.st_gid != 0:
        console.error("/etc/shadow is not group owned by root!")

    # RHEL-06-000035
    if stat.S_IMODE(shadow_file.st_mode) != 0:
        console.error("/etc/shadow is not mode 000!")


def gshadow_file_tests():
    # RHEL-06-000036
    gshadow_file = os.stat("/etc/gshadow")
    if gshadow_file.st_uid != 0:
        console.error("/etc/gshadow is not owned by root!")

    # RHEL-06-000037
    if gshadow_file.st_gid != 0:
        console.error("/etc/gshadow is not group owned by root!")

    # RHEL-06-000038
    if stat.S_IMODE(gshadow_file.st_mode) != 0:
        console.error("/etc/gshadow is not mode 000!")


def passwd_file_tests():
    # RHEL-06-000039
    passwd_file = os.stat("/etc/passwd")
    if passwd_file.st_uid != 0:
        console.error("/etc/passwd is not owned by root!")

    # RHEL-06-000040
    if passwd_file.st_gid != 0:
        console.error("/etc/passwd is not group owned by root!")

    # RHEL-06-000041
    if oct(stat.S_IMODE(passwd_file.st_mode)) != oct(0644):
        console.error("/etc/passwd is not mode 644!")


def group_file_tests():
    # RHEL-06-000042
    group_file = os.stat("/etc/group")
    if group_file.st_uid != 0:
        console.error("/etc/group is not owned by root!")

    # RHEL-06-000043
    if group_file.st_gid != 0:
        console.error("/etc/group is not group owned by root!")

    # RHEL-06-000044
    if oct(stat.S_IMODE(group_file.st_mode)) != oct(0644):
        console.error("/etc/group is not mode 644!")


def executable_file_tests():
    executable_locations = [
        "/bin",
        "/usr/bin",
        "/usr/local/bin",
        "/sbin",
        "/usr/sbin",
        "/usr/local/sbin"
    ]

    # RHEL-06-000047
    # next
    for location in executable_locations:

        for dirname, dirnames, filenames in os.walk(location):
            # for subdirname in dirnames:
            #     print os.path.join(dirname, subdirname)

            for filename in filenames:
                file_stats = os.stat(os.path.join(dirname, filename))

                if is_group_writable(file_stats):
                    console.error("System executable file %s is group writable!" % os.path.join(dirname, filename))
                    print oct(stat.S_IMODE(os.stat(os.path.join(dirname, filename)).st_mode))

                if is_world_writable(file_stats):
                    console.error("System executable file %s is world writable!" % os.path.join(dirname, filename))
                    print oct(stat.S_IMODE(os.stat(os.path.join(dirname, filename)).st_mode))


def rsyslog_file_tests():
    # RHEL-06-000133
    # RHEL-06-000134
    # RHEL-06-000135
    rsyslog_config_file = "/etc/rsyslog.conf"
    rsyslog_config = parsing.parse_rsyslog_config(rsyslog_config_file)

    for k, v in rsyslog_config.iteritems():

        # We want the log files so we get rid of other config
        if k.startswith("$"):
            continue

        # emerg.* gets written everywhere
        if v == "*":
            continue

        # Files that don't sync after every log are prefixed with "-"
        if v.startswith("-"):
            v = v.lstrip("-")

        log_stats = os.stat(v)

        if log_stats.st_uid != 0:
            console.error("%s is not owned by root!" % v)

        if log_stats.st_gid != 0:
            console.error("%s is not group owned by root!" % v)

        if (
            get_owner_permissions_int(log_stats) > 6 or
            get_group_permissions_int(log_stats) > 0 or
            get_world_permissions_int(log_stats) > 0
        ):
            console.error("Permissions are too open on %s" % v)


def run_tests():
    shadow_file_tests()
    gshadow_file_tests()
    passwd_file_tests()
    group_file_tests()
    executable_file_tests()
    rsyslog_file_tests()
