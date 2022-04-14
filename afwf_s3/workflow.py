# -*- coding: utf-8 -*-

import afwf
from .hdl import navigator

wf = afwf.Workflow()
wf.register(navigator.handler)
