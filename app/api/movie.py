# coding: utf-8
# Created by leo on 17-4-19.
"""
用于电影相关的操作
验证 想看 在看 看过 喜欢
添加
"""

from . import api
from app import mg
from flask import request
from app.models import User, Like, Wt, Rating
import json
from bson import ObjectId
from mongoengine.queryset.visitor import Q


@api.route('/movie/state', methods=['GET', 'POST'])
def state():
    """
    使用参数中的 id 和 uid 提取用户相关观看信息和喜欢信息
    :return: json
    """
    id = request.args.get('id')
    uid = request.args.get('uid')
    if uid == '0':
        return json.dumps({'status': 0, 'msg': 'user not found'})
    user = User.objects(id=ObjectId(uid)).first()
    if not user:
        return json.dumps({'status': 0, 'msg': 'user not found'})
    res = {
        'status': 200,
        'res': {
            'want': False,
            'watching': False,
            'watched': False,
            'like': False
        }
    }
    watch = Wt.objects(user=user)
    for w in watch:
        if w['value'] == id:
            if w['type'] == 'want':
                res['res']['want'] = True
            elif w['type'] == 'watching':
                res['res']['watching'] = True
            elif w['type'] == 'watched':
                res['res']['watched'] = True
    likes = Like.objects(user=user)
    for like in likes:
        if like['type'] == 'movie' and like['value'] == id:
            res['res']['like'] = True

    return json.dumps(res)


@api.route('/movie/change', methods=['GET', 'POST'])
def change():
    """
    更改用户 想看 在看 看过 相关信息
    :return:
    """
    uid = request.args.get('uid')
    mid = request.args.get('mid')
    movie_type = request.args.get('type')
    name = request.args.get('name')
    state = request.args.get('state')

    if uid == '0':
        return json.dumps({'status': 0, 'msg': 'user not found'})
    user = User.objects(id=ObjectId(uid)).first()
    if not user:
        return json.dumps({'status': 0, 'msg': 'user not found'})

    try:
        if state == 'true':  # add
            Wt(user=user, type=movie_type, value=mid, name=name).save()
        else:  # del
            Wt.objects(Q(user=user) & Q(type=movie_type) & Q(value=mid)).delete()
    except Exception, e:
        return json.dumps({'status': 2, 'msg': 'exception happened:' + e.message})

    return json.dumps({'status': 200, 'msg': 'success'})


@api.route('/movie/like/change', methods=['GET', 'POST'])
def like_change():
    """
    更改用户是否喜欢的相关信息
    :return:
    """
    uid = request.args.get('uid')
    mid = request.args.get('mid')
    like_type = request.args.get('type')
    name = request.args.get('name')
    state = request.args.get('state')

    if uid == '0':
        return json.dumps({'status': 0, 'msg': 'user not found'})
    user = User.objects(id=ObjectId(uid)).first()
    if not user:
        return json.dumps({'status': 0, 'msg': 'user not found'})

    try:
        if state == 'true':  # add
            Like(user=user, type=like_type, value=mid, name=name).save()
        else:  # del
            Like.objects(Q(user=user) & Q(type=like_type) & Q(value=mid)).delete()
    except Exception, e:
        return json.dumps({'status': 2, 'msg': 'exception happened:' + e.message})

    return json.dumps({'status': 200, 'msg': 'success'})






