# coding: utf-8
# Created by leo on 17-5-15.
"""
针对单部电影的推荐 API
"""
from flask import request
import json
from utils import res_return, RES_FILTER, LIMIT, CONTENTS_FILTER
from . import api
from app import mg
import numpy as np
import pandas as pd


@api.route('/rec/tags/<id>', methods=['GET', 'POST'])
def rec_by_tags(id):
    """
    按相同标签搜索电影,限定 20 部
    :param id: movieId
    :return: json
    """
    item = mg.db.movie.find_one({'_id': id})
    cursor = mg.db.movie.find({
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
    item = mg.db.movie.find_one({'_id': id})
    cursor = mg.db.movie.find({
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
    item = mg.db.movie.find_one({'_id': id})
    cursor = mg.db.movie.find({
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
    item = mg.db.movie.find_one({'_id': id})
    contents = []
    for i in xrange(2):
        cursor = mg.db.movie.find({'casts': {
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


@api.route('/rec/sum/')
def rec_sum():
    id = request.args.get('id')
    limit = int(request.args.get('limit') or 16)
    skip = int(request.args.get('skip') or 1)
    item = mg.db.movie.find_one({'_id': id})

    # 使用 pandas 的 DataFrame 处理数据
    # lens_id, genres, directors, writers, casts, sum
    # groupBy and sort_values
    genres_cursor = mg.db.movie.find({
        'genres': {"$in": item['genres']}
    }, RES_FILTER).limit(LIMIT * 3)
    genres = map(lambda x: [x['lens_id'], 1, 0, 0, 0], genres_cursor)

    directors_cursor = mg.db.movie.find({
        'directors': {"$in": item['directors']}
    }, RES_FILTER).limit(LIMIT)
    directors = map(lambda x: [x['lens_id'], 0, 2, 0, 0], directors_cursor)

    writers_cursor = mg.db.movie.find({
        'writers': {"$in": item['writers']}
    }, RES_FILTER).limit(LIMIT)
    writers = map(lambda x: [x['lens_id'], 0, 0, 1, 0], writers_cursor)

    contents = []
    casts_len = len(item['casts'])
    casts_iter = min(casts_len, 5)
    for i in xrange(casts_iter):
        cursor = mg.db.movie.find({'casts': {
            '$elemMatch': {
                'id': item['casts'][i]['id']
            }
        }}, RES_FILTER).limit(LIMIT)
        contents.extend(map(lambda x: [x['lens_id'], 0, 0, 0, 2], cursor))

    contents.extend(genres)
    contents.extend(directors)
    contents.extend(writers)

    data = np.array(contents)
    df = pd.DataFrame(data, columns=['lens_id', 'genres', 'directors', 'writers', 'casts'])
    group = df.groupby('lens_id').sum()
    group['sum'] = group.genres + group.directors + group.writers + group.casts
    movies = group.sort_values(by='sum', ascending=False)
    ids = movies.index.tolist()

    res = []
    for mv in ids:
        tmp = mg.db.movie.find_one({'lens_id': mv}, CONTENTS_FILTER)
        tmp['rank'] = movies.loc[mv].tolist().__str__()
        res.append(tmp)

    if len(res) == 0:
        return json.dumps({'status': 404})
    else:
        return json.dumps({
            'status': 200,
            'count': min(len(res), limit),
            'contents': res[skip:limit]
        })
