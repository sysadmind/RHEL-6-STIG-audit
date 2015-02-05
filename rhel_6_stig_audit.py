#!/usr/bin/env python
from tests import mounts, audit, packages, authentication, permissions

mounts.run_tests()
audit.run_tests()
packages.run_tests()
authentication.run_tests()
permissions.run_tests()
