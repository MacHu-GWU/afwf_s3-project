# -*- coding: utf-8 -*-

from typing import List
from s3pathlib import S3Path

from .cache import cache
from .boto_ses import bsm


@cache.memoize(expire=1)
def list_buckets() -> List[str]:
    bucket_list = list()
    res = bsm.s3_client.list_buckets()
    for dct in res.get("Buckets", list()):
        bucket_name = dct["Name"]
        bucket_list.append(bucket_name)
    return bucket_list


@cache.memoize(expire=1)
def list_objects(prefix_uri: str) -> List[str]:
    return [
        s3path.uri
        for s3path in S3Path.from_s3_uri(prefix_uri).iter_objects(bsm=bsm)
    ]


if bsm.aws_region in {"us-gov-east-1", "us-gov-west-1"}:
    def get_console_url(s3path: S3Path):
        return s3path.us_gov_cloud_console_url
else:
    def get_console_url(s3path: S3Path):
        return s3path.console_url
