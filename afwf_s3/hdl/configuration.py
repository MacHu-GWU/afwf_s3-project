# -*- coding: utf-8 -*-

import attr
import afwf


@attr.define
class SetAWSProfileHandler(afwf.Handler):
    def lower_level_api(self, **kwargs) -> afwf.ScriptFilter:
        pass


handler = SetAWSProfileHandler(id="set-aws-profile-handler")