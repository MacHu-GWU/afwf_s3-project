# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from s3pathlib import S3Path
from pathlib_mate import Path
from afwf_s3.hdl.navigator import handler as hdl
from afwf_s3.tests import bsm, s3path_prefix
from pprint import pprint


class TestHandler:
    def test(self):
        sf = hdl.lower_level_api("")
        assert len(sf.items) >= 1
        assert s3path_prefix.bucket in [item.title for item in sf.items]

        sf = hdl.lower_level_api(s3path_prefix.bucket)
        assert len(sf.items) >= 1
        assert s3path_prefix.bucket in [item.title for item in sf.items]

        sf = hdl.lower_level_api(f"{s3path_prefix.bucket}/")
        assert len(sf.items) >= 1
        assert f"{s3path_prefix.parts[0]}/" in [item.title for item in sf.items]

        sf = hdl.lower_level_api(f"{s3path_prefix.bucket}/{s3path_prefix.key}")
        assert len(sf.items) == 5

    def test_list_objects(self):
        item_list = list(hdl.list_objects(s3path_prefix))
        assert len(item_list) == 5

        item_list = list(hdl.list_objects(S3Path(s3path_prefix, "data")))
        assert len(item_list) == 4

        item_list = list(hdl.list_objects(S3Path(s3path_prefix, "dataset")))
        assert len(item_list) == 3

        item_list = list(hdl.list_objects(S3Path(s3path_prefix, "READ")))
        assert len(item_list) == 1

        item_list = list(hdl.list_objects(S3Path(s3path_prefix, "datalake")))
        assert len(item_list) == 1

        item_list = list(hdl.list_objects(S3Path(s3path_prefix, "datalake/")))
        assert len(item_list) == 2


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
