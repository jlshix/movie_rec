# coding: utf-8
# Created by leo on 17-4-19.
count = 36
num = 8
step = count/num
index = [0].extend([])
for num in xrange(1, count):
    print [x for x in xrange(count) if x % num == 0]
