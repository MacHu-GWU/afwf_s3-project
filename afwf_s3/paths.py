# -*- coding: utf-8 -*-

from pathlib_mate import Path
from .runtime import IS_LOCAL_DEV, IS_ALFRED, IS_CI

DIR_HOME = Path.home()
DIR_AFWF_S3 = Path(DIR_HOME, ".alfred-afwf_s3")
DIR_CACHE = Path(DIR_AFWF_S3, ".cache")
PATH_SETTINGS_DB = Path(DIR_AFWF_S3, "settings.sqlite")

PATH_AWS_CONFIG_FILE = Path(DIR_HOME, ".aws", "credentials")
PATH_AWS_CREDENTIAL_FILE = Path(DIR_HOME, ".aws", "config")

DIR_AFWF_S3_PYTHON_LIB = Path.dir_here(__file__)

