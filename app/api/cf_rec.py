# coding: utf-8
# Created by leo on 17-5-15.
"""
协同过滤推荐 API
"""
import json
from . import api
from app import mg, recommender
from flask import request


@api.route('/cf/', methods=['GET', 'POST'])
def cf_by_user():
    """
    按相同标签搜索电影,限定 20 部
    :param uid: userId
    :param n: movieCount
    :return: json
    """
    uid = request.args.get('uid') or "1"
    n = int(request.args.get('n') or 8)

    recs = recommender.top_n(uid, n)
    contents = [{"title": rec[0], "rating": rec[1], "count": rec[2]} for rec in recs]
    return json.dumps({
        'status': 200,
        'contents': contents
    })