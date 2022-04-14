# -*- coding: utf-8 -*-

import sys
from s3pathlib import S3Path, context
from pathlib_mate import Path

from ..runtime import RUNTIME
from ..boto_ses import bsm

bucket = "aws-data-lab-sanhe-for-opensource"
prefix = "unittest/afwf_s3/runtime={runtime}/platform={os}/py{major}{minor}".format(
    runtime=RUNTIME,
    os=sys.platform,
    major=sys.version_info.major,
    minor=sys.version_info.minor
)

s3path_prefix = S3Path(bucket, prefix).to_dir()
dir_bucket = Path.dir_here(__file__).append_parts("folder")

context.attach_boto_session(bsm.boto_ses)
if not s3path_prefix.exists():
    s3path_prefix.upload_dir(dir_bucket.abspath)
