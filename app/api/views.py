# coding: utf-8
# Created by leo on 17-4-13.
"""
主要是返回json的视图们
(因为是API啊)
"""
from flask import request
from . import api
from app import mg
import json
import re


@api.route('/subject/<id>', methods=['GET', 'POST'])
def subject(id):
    cursor = mg.db.spider.find({'_id': id})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    elif cursor.count() == 1:
        return json.dumps(list(cursor)[0])
    else:
        return json.dumps({'status': 500})


@api.route('/genres/<tag>', methods=['GET', 'POST'])
def genres(tag):
    cursor = mg.db.spider.find({'genres': {'$in': [tag]}})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/year/<tag>', methods=['GET', 'POST'])
def year(tag):
    cursor = mg.db.spider.find({'year': tag})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/country/<tag>', methods=['GET', 'POST'])
def country(tag):
    cursor = mg.db.spider.find({'countries': {'$in': [tag]}})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/director/<tag>', methods=['GET', 'POST'])
def director(tag):
    tag = str(tag).replace('', '·')
    pat = re.compile(tag)
    cursor = mg.db.spider.find({'directors.name': {'$in': [pat]}})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/actor/<tag>', methods=['GET', 'POST'])
def actor(tag):
    tag = unicode(tag).replace(' ', u'·')
    pat = re.compile(tag)
    cursor = mg.db.spider.find({'casts.name': {'$in': [pat]}})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/writer/<tag>', methods=['GET', 'POST'])
def writer(tag):
    tag = unicode(tag).replace(' ', u'·')
    pat = re.compile(tag)
    cursor = mg.db.spider.find({'writers.name': {'$in': [pat]}})
    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list(x['title'] for x in cursor.limit(100))
        }
        return json.dumps(res)


@api.route('/rating', methods=['GET', 'POST'])
def rating():
    average = request.args.get('average')
    count = request.args.get('count')
    query = {}
    if average:
        query['rating.average'] = {'$gte': average}
    if count:
        query['rating.rating_people'] = {'$gte': count}
    if len(query) == 0:
        return json.dumps({'status': 1, 'msg': 'param problems'})
    else:
        cursor = mg.db.spider.find(query)

    if cursor.count() == 0:
        return json.dumps({'status': 404})
    else:
        res = {
            'status': 200,
            'count': cursor.count(),
            'contents': list((x['title'], x['rating']['average'], x['rating']['rating_people']) for x in cursor.limit(100))
        }
        return json.dumps(res)

