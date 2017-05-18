# coding: utf-8
# Created by leo on 17-5-15.
import json

RES_FILTER = {
        'id': 1,
        'title': 1,
        'rating.average': 1
    }
LIMIT = 20


def res_return(cursor):
    """
    在 View 中的统一返回
    :param cursor:
    :return:
    """
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        return json.dumps({
            'status': 200,
            'count': cursor.count(),
            'contents': list(cursor)
        })
