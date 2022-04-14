# -*- coding: utf-8 -*-

from diskcache import Cache
from .paths import DIR_AFWF_S3, DIR_CACHE

DIR_AFWF_S3.mkdir_if_not_exists()


class CustomCache(Cache):
    def fast_get(self, key, callable, kwargs=None, expire=None):
        value = self.get(key)
        if value is None:
            if kwargs is None:
                kwargs = {}
            value = callable(**kwargs)
            self.set(key, value, expire=expire)
        return value


cache = CustomCache(DIR_CACHE.abspath)


class CacheKeys:
    aws_profile_list_from_config = None
    aws_profile_and_region_list_from_config = None


for k in CacheKeys.__dict__.keys():
    if not k.startswith("_"):
        setattr(CacheKeys, k, k)
