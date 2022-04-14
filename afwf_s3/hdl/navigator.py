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
    def list_all_bucket(self) -> Iterable[afwf.Item]:
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
            yield item

    def filter_bucket(self, bucket_name_query: str) -> Iterable[afwf.Item]:
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
            yield item

    def s3path_to_item(self, s3path: S3Path) -> afwf.Item:
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

    def list_objects(self, s3path_prefix: S3Path) -> Iterable[afwf.Item]:
        for s3path in s3path_prefix.iterdir(bsm=bsm):
            yield self.s3path_to_item(s3path)

    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """

        s3
        :param kwargs:
        :return:
        """
        chunks = query.split("/")
        if len(chunks) == 0:
            raise NotImplementedError
        elif len(chunks) == 1:
            if len(chunks[0].strip()): # "my-buck" or "my-bucket"
                iterator = self.filter_bucket(bucket_name_query=chunks[0])
            else: # ""
                iterator = self.list_all_bucket()
        elif len(chunks) >= 2:
            s3path_prefix = S3Path(chunks[0], "/".join(chunks[1:]))
            iterator = self.list_objects(s3path_prefix)
        else:
            raise NotImplementedError
        sf = afwf.ScriptFilter()
        for item in iterator:
            sf.items.append(item)
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="navigator")
