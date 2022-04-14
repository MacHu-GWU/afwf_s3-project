# -*- coding: utf-8 -*-

from typing import List, Dict, Iterable

import attr
import afwf
from afwf.query import parse_query
from s3pathlib import S3Path
from ..boto_ses import bsm
from ..cache import cache
from ..s3 import list_buckets, list_objects, get_console_url
from ..fuzzy_filter import FuzzyObjectSearch
from afwf.workflow import log_debug_info


@attr.define
class Handler(afwf.Handler):
    def list_all_bucket(
        self,
        sf: afwf.ScriptFilter,
    ):
        for bucket in list_buckets():
            s3path = S3Path(bucket)
            item = afwf.Item(
                title=bucket,
                subtitle="open S3 console",
                arg=bucket,
                autocomplete=bucket,
                uid=f"s3://{bucket}",
            )
            item.open_url(url=get_console_url(s3path))
            item.add_modifier(
                mod=afwf.ModEnum.alt.value,
                subtitle="Hit Enter to copy 'arn' to clipboard asdfasdfasdf",
                arg=f"arn:aws:s3:::{bucket}",
            )
            item.add_modifier(
                mod=afwf.ModEnum.shift.value,
                subtitle="Hit Enter to copy 's3 uri' to clipboard",
                arg=f"s3://{bucket}/",
            )
            sf.items.append(item)

    def filter_bucket(
        self,
        sf: afwf.ScriptFilter,
        bucket_name_query: str,
    ):
        bucket_list = list_buckets()
        fs = FuzzyObjectSearch(
            keys=bucket_list,
            mapper={bucket: bucket for bucket in bucket_list},
        )
        filtered_bucket_list = fs.match(bucket_name_query, limit=100)

        for bucket in filtered_bucket_list:
            s3path = S3Path(bucket)
            item = afwf.Item(
                title=bucket,
                subtitle="open S3 console",
                arg=bucket,
                autocomplete=bucket,
                uid=f"s3://{bucket}",
            )
            item.open_url(url=get_console_url(s3path))
            item.add_modifier(
                mod=afwf.ModEnum.alt.value,
                subtitle="Hit Enter to copy 'arn' to clipboard",
                arg=f"arn:aws:s3:::{bucket}",
            )
            item.add_modifier(
                mod=afwf.ModEnum.shift.value,
                subtitle="Hit Enter to copy 's3 uri' to clipboard",
                arg=f"s3://{bucket}/",
            )
            sf.items.append(item)

    def s3path_to_item(
        self,
        s3path: S3Path,
    ) -> afwf.Item:
        if s3path.is_dir():
            title = s3path.basename + "/"
        else:
            title = s3path.basename
        item = afwf.Item(
            title=title,
            subtitle=s3path.uri,
            arg=s3path.uri,
            autocomplete=s3path.uri.replace("s3://", "", 1),
            uid=s3path.uri,
        )
        item.open_url(url=get_console_url(s3path))
        item.add_modifier(
            mod=afwf.ModEnum.alt.value,
            subtitle="Hit Enter to copy 'arn' to clipboard",
            arg=f"arn:aws:s3:::{s3path.bucket}/{s3path.key}",
        )
        return item

    def list_objects(
        self,
        sf: afwf.ScriptFilter,
        s3path_prefix: S3Path,
    ):
        for s3path in s3path_prefix.iterdir(bsm=bsm):
            sf.items.append(self.s3path_to_item(s3path))

    def show_account_info(
        self,
        sf: afwf.ScriptFilter,
    ):
        iam_client = bsm._get_client("iam")
        account_aliases = iam_client.list_account_aliases(). \
            get("AccountAliases", list())
        if len(account_aliases):
            account_alias = account_aliases[0]
        else:
            account_alias = "unknwon"
        item = afwf.Item(
            title=f"{bsm.aws_account_id}, {bsm.aws_region}",
            subtitle=f"account alias: {account_alias}",
            arg=bsm.aws_account_id,
        )
        sf.items.append(item)

    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """

        s3
        :param kwargs:
        :return:
        """
        chunks = query.split("/")
        sf = afwf.ScriptFilter()
        if len(chunks) == 0:
            raise NotImplementedError
        elif len(chunks) == 1:
            q = chunks[0].strip()
            if len(q):  # "my-buck" or "my-bucket"
                if q == "?":
                    self.show_account_info(sf)
                else:
                    self.filter_bucket(sf, bucket_name_query=chunks[0])
            else:  # ""
                self.list_all_bucket(sf)
        elif len(chunks) >= 2:
            s3path_prefix = S3Path(chunks[0], "/".join(chunks[1:]))
            self.list_objects(sf, s3path_prefix)
        else:
            raise NotImplementedError

        if len(sf.items) == 0:
            sf.items.append(afwf.Item(
                title="No result found!",
                icon=afwf.Icon.from_image_file(afwf.Icons.error)
            ))
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="navigator")
