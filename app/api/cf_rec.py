# coding: utf-8
# Created by leo on 17-5-15.
"""
协同过滤推荐 API
"""
import json
from . import api
from app import mg, recommender


@api.route('/cf/<int:uid>/<int:n>', methods=['GET', 'POST'])
def cf_by_user(uid, n):
    """
    按相同标签搜索电影,限定 20 部
    :param uid: userId
    :param n: movieCount
    :return: json
    """
    res = recommender.top_n(uid, n)
    return json.dumps(res)