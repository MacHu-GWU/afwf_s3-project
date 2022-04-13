# -*- coding: utf-8 -*-

from chalice import Chalice
from afwf_s3.lbd import hello

app = Chalice(app_name="afwf_s3")


@app.lambda_function(name="hello")
def handler_hello(event, context):
    return hello.high_level_api(event, context)
