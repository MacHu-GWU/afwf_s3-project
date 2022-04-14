# -*- coding: utf-8 -*-

import pytest
from afwf_s3.s3 import (
    list_buckets,
    list_objects,
)
from afwf_s3.tests import bucket, prefix, s3path_prefix


def test_list_buckets():
    _ = list_buckets()


def test_list_objects():
    res = list_objects(s3path_prefix.uri)
    assert len(res) == 11


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
