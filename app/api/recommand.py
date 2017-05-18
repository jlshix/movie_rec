# coding: utf-8
# Created by leo on 17-5-15.
"""
推荐 API
"""
import json
from operator import add
from utils import res_return, RES_FILTER, LIMIT
from . import api
from app import mg, sc


@api.route('/rec/tags/<id>', methods=['GET', 'POST'])
def rec_by_tags(id):
    """
    按相同标签搜索电影,限定 20 部
    :param id: movieId
    :return: json
    """
    item = mg.db.spider.find_one({'_id': id})
    cursor = mg.db.spider.find({
        'genres': item['genres']
    }, RES_FILTER).limit(LIMIT)
    return res_return(cursor)


@api.route('/rec/directors/<id>', methods=['GET', 'POST'])
def rec_by_directors(id):
    """
    按相同导演搜索电影,限定 20 部
    :param id: movieId
    :return: json
    """
    item = mg.db.spider.find_one({'_id': id})
    cursor = mg.db.spider.find({
        'directors': item['directors']
    }, RES_FILTER).limit(LIMIT)
    return res_return(cursor)


@api.route('/rec/writers/<id>', methods=['GET', 'POST'])
def rec_by_writers(id):
    """
    按相同编剧搜索电影,限定 20 部
    :param id: movieId
    :return: json
    """
    item = mg.db.spider.find_one({'_id': id})
    cursor = mg.db.spider.find({
        'writers': item['writers']
    }, RES_FILTER).limit(LIMIT)
    return res_return(cursor)


@api.route('/rec/casts/<id>', methods=['GET', 'POST'])
def rec_by_casts(id):
    """
    按相同演员搜索电影,前三个每人限定 20 部
    :param id: movieId
    :return: json
    """
    item = mg.db.spider.find_one({'_id': id})
    contents = []
    for i in xrange(2):
        cursor = mg.db.spider.find({'casts': {
            '$elemMatch': {
                'id': item['casts'][i]['id']
            }
        }}, RES_FILTER).limit(LIMIT)
        contents.extend(list(cursor))

    if len(contents) == 0:
        return json.dumps({'status': 404})
    else:
        return json.dumps({
            'status': 200,
            'count': len(contents),
            'contents': contents
        })


@api.route('/rec/sum/<id>')
def rec_sum(id):
    item = mg.db.spider.find_one({'_id': id})
    genres_cursor = mg.db.spider.find({
        'genres': item['genres']
    }, RES_FILTER).limit(LIMIT)
    directors_cursor = mg.db.spider.find({
        'directors': item['directors']
    }, RES_FILTER).limit(LIMIT)
    writers_cursor = mg.db.spider.find({
        'writers': item['writers']
    }, RES_FILTER).limit(LIMIT)

    contents = []
    for i in xrange(2):
        cursor = mg.db.spider.find({'casts': {
            '$elemMatch': {
                'id': item['casts'][i]['id']
            }
        }}, RES_FILTER).limit(LIMIT)
        contents.extend(list(cursor))

    contents.extend(list(genres_cursor))
    contents.extend(list(directors_cursor))
    contents.extend(list(writers_cursor))

    rdd = sc.parallelize([x['_id'] for x in contents])
    tmp = rdd.map(lambda x: (x, 1))\
        .reduceByKey(add)\
        .sortBy(lambda x: x[1], False)\
        .map(lambda x: x[0])\
        .toLocalIterator()
    res = []
    tlist = []
    for c in contents:
        if c not in tlist:
            tlist.append(c)
    for t in tmp:
        for c in tlist:
            if c['_id'] == t:
                res.append(c)

    if len(res) == 0:
        return json.dumps({'status': 404})
    else:
        return json.dumps({
            'status': 200,
            'count': len(res),
            'contents': res
        })

