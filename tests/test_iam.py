# -*- coding: utf-8 -*-

import pytest
from afwf_s3.boto_ses import bsm

def test():
    iam_client = bsm._get_client("iam")

    res = iam_client.list_account_aliases()




if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
