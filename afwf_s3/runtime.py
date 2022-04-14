# -*- coding: utf-8 -*-

"""
Identify the current runtime.
"""

import os
from pathlib_mate import Path


class Runtime:
    local_dev = "local_dev"
    alfred = "alfred"
    ci = "ci"


IS_LOCAL_DEV = False
IS_ALFRED = False
IS_CI = False

if "CI" in os.environ:
    RUNTIME = Runtime.ci
    IS_CI = True
else:
    dir_here = Path.dir_here(__file__)
    if dir_here.parent.parent.basename.startswith("user.workflow."):
        RUNTIME = Runtime.alfred
        IS_ALFRED = True
    else:
        RUNTIME = Runtime.local_dev
        IS_LOCAL_DEV = True
