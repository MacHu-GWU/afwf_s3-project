# -*- coding: utf-8 -*-

import os
import boto3
from s3pathlib import BotoSesManager
from .runtime import IS_LOCAL_DEV, IS_ALFRED, IS_CI

if IS_LOCAL_DEV:
    _boto_ses = boto3.session.Session(
        profile_name="aws_data_lab_sanhe_opensource_afwf_s3",
    )
elif IS_ALFRED:
    _boto_ses = boto3.session.Session()
elif IS_CI:
    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID_FOR_GITHUB_CI"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY_FOR_GITHUB_CI"]
    _boto_ses = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"
    )
else:  # pragma: no cover
    raise NotImplementedError

bsm = BotoSesManager(boto_ses=_boto_ses)
