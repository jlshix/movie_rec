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
    :param uid: userId
    :param n: movieCount
    :return: json
    """
    uid = request.args.get('uid') or "1"
    n = int(request.args.get('n') or 8)

    contents = []
    recs = recommender.top_n(uid, n)
    print recs
    print recs[0]
    print recs[0][0]
    print type(recs[0][0])

    for rec in recs:
        tmp = dict(zip(('mid', 'title', 'rating', 'count'), rec))
        poster = mg.db.movie.find_one({'lens_id': tmp['mid']})['poster']
        tmp['poster'] = poster
        contents.append(tmp)

    return json.dumps({
        'status': 200,
        'contents': contents
    })