# coding: utf-8
# Created by leo on 17-4-12.

from app import mg

col = mg.db.spider

# 按照名称搜索
title = '爱乐之城'
q1 = col.find({'title': {'$regex': title}})
print q1.count()

