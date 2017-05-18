# coding: utf-8
# Created by leo on 17-4-19.

import os
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


conf = SparkConf().setAppName('TEST').setMaster('local[*]')
sc = SparkContext(conf=conf)

log.info('Loading data...')

ratings_raw = sc.textFile('ml-latest-small/ratings.csv')
# take 返回一个列表 用[0]还是取第一个
ratings_raw_header = ratings_raw.take(1)[0]
# ratings 结构为 (userId, movieId, rating, timestamp)
ratings_rdd = ratings_raw.filter(lambda line: line != ratings_raw_header)\
    .map(lambda line: line.split(','))\
    .map(lambda items: (int(items[0]), int(items[1]), float(items[2]))).cache()

log.info('ratings data done...')

movies_raw = sc.textFile('ml-latest-small/movies.csv')
movies_raw_header = movies_raw.take(1)[0]
# movies 结构为 (movieId, title, genres)
movies_rdd = movies_raw.filter(lambda line: line != ratings_raw_header)\
    .map(lambda line: line.split(','))\
    .map(lambda item: (int(item[0]), item[1], item[2])).cache()
movies_title_rdd = movies_rdd.map(lambda item: (int(item[0]), item[1])).cache()

log.info('movies data done.')



