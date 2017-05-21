# coding: utf-8
# Created by leo on 17-5-18.

from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Recommender(object):

    def __init__(self, app=None):
        self.rank = 8
        self.seed = 5L
        self.iterations = 10
        self.regularization_parameter = 0.1

    def init_app(self, mg):

        """
        初始化函数 读入电影和评分,生成 RDD
        :param mg: mongodb
        """
        # 初始化 mongodb 和 spark
        log.info('Initializing recommender...')
        client = MongoClient('localhost', 27017)
        self.col = client['mr']['rating']
        conf = SparkConf().setAppName('movie_rec').setMaster('local[*]')
        self.sc = SparkContext(conf=conf)

        # 查询数据库中的评分数据
        log.info('Querying mongodb data...')
        query = self.col.find(
            {},
            {'_id': 0, 'uid': 1, 'mid': 1, 'rating': 1}
        )
        qlist = [(x['uid'], x['mid'], x['rating']) for x in query]
        self.mg_ratings_rdd = self.sc.parallelize(qlist)

        # 载入 movielens 数据
        log.info('loading ratings data...')
        # ratings_raw = sc.textFile(path_to_file + 'ratings/*')
        ratings_raw = self.sc.textFile('ratings.csv')
        log.info(ratings_raw.take(6))
        # take 返回一个列表 用[0]还是取第一个
        ratings_raw_header = ratings_raw.take(1)[0]
        # ratings 结构为 (userId, movieId, rating, timestamp)
        # 去掉文件头 -> 每行以逗号分割变为一个列表 -> 转为相应的数据类型 -> 合并数据库数据
        self.ratings_rdd = ratings_raw.filter(lambda line: line != ratings_raw_header) \
            .map(lambda line: line.split(',')) \
            .map(lambda items: (int(items[0]), int(items[1]), float(items[2])))\
            .union(self.mg_ratings_rdd).cache()
        log.info('ratings data done...')

        # movies_raw = sc.textFile(path_to_file + 'movies/*')
        movies_raw = self.sc.textFile('movies.csv')
        movies_raw_header = movies_raw.take(1)[0]
        # movies 结构为 (movieId, title, genres)
        self.movies_rdd = movies_raw.filter(lambda line: line != movies_raw_header) \
            .map(lambda line: line.split(',')) \
            .map(lambda item: (int(item[0]), item[1], item[2])).cache()

        self.titles_rdd = self.movies_rdd.map(lambda item: (int(item[0]), item[1])).cache()

        log.info('movies data done.')
        self.__rating_count_and_avg()
        self.__train_model()

    def __rating_count_and_avg(self):
        """
        根据电影 RDD 获取评分总数和平均评分
        """
        log.info('calculating rating count and average rating...')
        # 转为 (movieId, rating) 并按 movieId 分组
        # 每组都是 (id [r1, r2, ...])
        # 返回 (id, count, avg)
        self.id_count_avg_rdd = self.ratings_rdd.map(lambda x: (x[1], x[2])).groupByKey()\
            .map(lambda item: (
                item[0], len(item[1]), float(sum(x for x in item[1]) / len(item[1]))
        ))
        self.id_count_rdd = self.id_count_avg_rdd.map(lambda x: (x[0], x[1]))
        log.info('done rating count and average rating.')

    def __train_model(self):
        log.info('training model...')
        self.model = ALS.train(
            ratings=self.ratings_rdd,
            rank=self.rank,
            iterations=self.iterations,
            lambda_=self.regularization_parameter,
            seed=self.seed
        )
        log.info('done training model.')

    def __predict(self, user_movie_rdd):
        """
        对给定的 (userId, movieId) 进行预测
        :param user_movie_rdd:
        :return: (title, rating, count)
        """
        # (mid, rating).(mid, title) -> (mid, (rating, title))
        # (mid, (rating, title)).(mid, count) -> (mid, ((rating, title), count))
        predicted_movie_rating = self.model.predictAll(user_movie_rdd)\
            .map(lambda x: (x.product, x.rating))
        title_rating_count = predicted_movie_rating.join(self.titles_rdd)\
            .join(self.id_count_rdd).map(lambda x: (x[1][0][1], x[1][0][0], x[1][1]))
        return title_rating_count

    def add_ratings(self, ratings):
        """
        增加新的评分数据
        :param ratings:
        """
        new_rdd = self.sc.parallelize(ratings)
        self.ratings_rdd = self.ratings_rdd.union(new_rdd)
        self.__rating_count_and_avg()
        self.__train_model()

    def predict_for_user(self, uid, movie_ids):
        """
        预测用户评分
        :param uid: userId
        :param movie_ids: [movieId1, movieId2, ...]
        :return: [(movieId1, rating1), (movieId2, rating2), ...]
        """
        uid_movie_rdd = self.sc.parallelize(movie_ids).map(lambda x: (uid, x))
        return self.__predict(uid_movie_rdd)

    def top_n(self, uid, n):
        """
        为用户推荐 n 部电影
        :param uid: userId
        :param n: number of movies
        :return: predict
        """
        log.info('doing top_n...')
        uid_movie_rdd = self.ratings_rdd.filter(lambda x: x[0] != uid)\
            .map(lambda x: (uid, x[1])).distinct()

        top_n = self.__predict(uid_movie_rdd)\
            .filter(lambda r: r[2] >= 25).takeOrdered(n, key=lambda x: -x[1])
        log.info('done top_n...')
        return top_n
