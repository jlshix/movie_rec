# coding: utf-8
# Created by leo on 17-4-19.

from faker import Faker
from pymongo import MongoClient
from app.models import User, Like, Watch, Comments
from random import randint
import json
from datetime import datetime


mg = MongoClient('localhost', 27017)
db = mg.movie
fake = Faker()


def get_likes(num):
    res = []
    count = db.spider.count()
    query = db.spider.find({}, {'_id': 1, 'title': 1}).skip(count/randint(1, 10)).limit(num)
    for i in xrange(num):
        like = Like()
        like.type = 'movie'
        like.name = query[i]['title']
        like.value = query[i]['_id']
        res.append(like)
    return res


def get_watch(num):
    res = []
    count = db.spider.count()
    query = db.spider.find({}, {'_id': 1, 'title': 1}).skip(count / randint(1, 10)).limit(num)
    for i in xrange(num):
        watch = Watch()
        no = randint(0, 2)
        watch.type = ['want', 'watching', 'watched'][no]
        watch.name = query[i]['title']
        watch.value = query[i]['_id']
        res.append(watch)
    return res


def get_comments(num):
    res = []
    count = db.spider.count()
    query = db.spider.find({}, {'_id': 1}).skip(count / randint(1, 10)).limit(num)
    for i in xrange(num):
        comment = Comments()
        comment.mid = query[i]['_id']
        comment.title = fake.sentence()
        comment.content = '\n'.join(fake.sentences(nb=randint(2, 7)))
        res.append(comment)
    return res


def get_interests(num):
    interests = ["爱情", "喜剧", "剧情", "动画", "科幻", "动作", "经典", "悬疑", "青春", "犯罪", "惊悚", "文艺", "搞笑", "纪录片", "励志", "恐怖", "战争", "短片", "黑色幽默", "魔幻", "传记", "情色", "感人", "暴力", "家庭", "音乐", "动画短片", "童年", "浪漫", "女性", "黑帮", "同志", "史诗", "烂片", "童话", "西部"]
    res = []
    for i in xrange(num):
        ri = randint(0, len(interests) - 1)
        res.append(interests.pop(ri))
    return res


for ix in xrange(1):
    user = User()
    user.name = fake.user_name()
    user.email = fake.safe_email()
    user.password = '1234'
    user.confirmed = randint(0, 3) % 2 == 0
    user.since = fake.date_time()
    user.gender = randint(0, 3) % 2 == 0
    user.likes = get_likes(randint(5, 10))
    user.watch = get_watch(randint(10, 100))
    user.comments = get_comments(randint(2, 10))
    user.interests = get_interests(randint(2, 6))
    # print user.to_json()
    # print user.to_mongo()
    # db.user.insert_one(json.loads(user.to_json()))
    print datetime.utcnow()
    print type(datetime.utcnow())
    

