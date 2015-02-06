from __future__ import print_function
import sys

BLUE = '\033[94m'
OK = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[91m'
ENDC = '\033[0m'


def error(*objs):
    print(ERROR, "ERROR: ", ENDC, *objs, file=sys.stderr)


def warning(*objs):
    print(WARNING, "WARNING: ", ENDC, *objs, file=sys.stderr)


def ok(*objs):
    print(OK, "OK: ", ENDC, *objs, file=sys.stderr)


def heading(name):
    print(BLUE, '{0:*^50}'.format(name), ENDC)
