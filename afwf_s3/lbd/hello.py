# -*- coding: utf-8 -*-

import traceback


def low_level_api(name):
    if name is None:
        return "Hello Mr X"
    else:
        return "Hello {}".format(name)


def high_level_api(event, context):
    try:
        message = low_level_api(name=event["name"])
        return {
            "message": message,
            "data": {"message": message},
            "error": None,
        }
    except Exception:
        return {
            "message": "something wrong!",
            "data": None,
            "error": {
                "traceback": traceback.format_exc()
            }
        }
