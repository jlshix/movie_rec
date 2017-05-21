# coding: utf-8
# Created by leo on 17-4-8.
"""
辅助工具
"""
import requests
from bs4 import BeautifulSoup
from flask import abort
from math import ceil
import json
from app import recommender, mg
from operator import add

RES_FILTER = {
        'id': 1,
        'title': 1,
        'rating.average': 1
    }
LIMIT = 20


def add_douban_movie(id):
    """
    从豆瓣获取新电影
    :param id: subject id
    :return: dict
    """
    url = 'https://movie.douban.com/subject/'
    r = requests.get(url + id)
    soup = BeautifulSoup(r.text, 'lxml')

    content = soup.find("div", id="content")
    # 无链接的列表类型
    list_items = {
        # 'directors': '导演', 'writers': '编剧', 'casts': '主演',
        'genres': '类型', 'countries': '制片国家/地区', 'languages': '语言',
        'aka': '又名'
    }
    # 无链接的字符串类型
    single_items = {
        'season_count': '季数', 'episodes': '集数', 'site': '官方网站',
        'douban_site': '官方小站', 'imdb': 'IMDb链接'
    }

    # 标题
    name_and_year = [item.get_text() for item in content.find("h1").find_all("span")]
    name, year = name_and_year if len(name_and_year) == 2 else (name_and_year[0], "")

    # 字典存储movie便于存入数据库
    movie = {
        '_id': str(url).split('/')[-2],
        'title': name.strip(),
        'year': year.strip('()')
    }

    # 左边
    content_left = soup.find("div", class_="subject clearfix")

    nbg_soup = content_left.find("a", class_="nbgnbg").find("img")
    # 海报
    movie['poster'] = nbg_soup.get("src") if nbg_soup else ""
    info = content_left.find("div", id="info").get_text()
    info_dict = dict([line.strip().split(":", 1) for line in info.strip().split("\n") if line.strip().find(":") > 0])

    for key, value in list_items.items():
        movie[key] = info_dict.get(value, '').replace('\t', '').strip().split(' / ')
    for key, value in single_items.items():
        movie[key] = info_dict.get(value, '').replace('\t', '').strip()

    # 带链接的列表类型处理
    dwc_info = content_left.find("div", id="info")
    directors_field = dwc_info.find_all('a', rel='v:directedBy')
    writers_field = dwc_info.find_all('a', rel='')
    casts_field = dwc_info.find_all('a', rel='v:starring')

    directors = []
    for director_field in directors_field:
        directors.append({'id': director_field.get('href').split('/')[-2], 'name': director_field.get_text()})
    movie['directors'] = directors
    writers = []
    for writer_field in writers_field:
        writers.append({'id': writer_field.get('href').split('/')[-2], 'name': writer_field.get_text()})
    movie['writers'] = writers
    casts = []
    for cast_field in casts_field:
        casts.append({'id': cast_field.get('href').split('/')[-2], 'name': cast_field.get_text()})
    movie['casts'] = casts

    # 名称有变化的类型处理
    pubdate = '上映日期' if '上映日期' in info_dict else '首播'
    movie['pubdate'] = info_dict.get(pubdate, "").replace("\t", " ").strip().split(' / ')
    duration = '片长' if '片长' in info_dict else '单集片长'
    movie['duration'] = info_dict.get(duration, "").replace("\t", " ").split('分')[0].strip()

    # 右边
    content_right = soup.find("div", class_="rating_wrap clearbox")
    if content_right:
        # 评分
        rating_sum = content_right.find("strong", class_="ll rating_num").get_text()
        # 参评人数
        rating_people = content_right.find("a", class_="rating_people")
        rating_people = rating_people.find("span").get_text() if rating_people else ""
        # 评分详情
        rating_per_list = [item.get_text().strip('%') for item in content_right.find_all("span", class_="rating_per")]
        movie['rating'] = {
            'average': rating_sum,
            'rating_people': rating_people,
            'stars': rating_per_list
        }
    else:
        movie['rating'] = {
            'average': '',
            'rating_people': '',
            'stars': ''
        }

    # 下边
    summary = soup.find('span', property='v:summary').get_text().strip()
    movie['summary'] = summary.replace(' ', '').replace('\n\u3000\u3000', '')

    assert len(movie) == 20, "length of movie is invalid"

    return movie


def paginate(query, page, per_page, err_out):
    """
    MongoDB 分页 参考 SQLALCHEMY
    :param query: 查询游标
    :param page: 当前页
    :param per_page: 每页数量
    :param err_out: 查询至最后是 404 还是 空
    :return: Pagination()
    """

    if err_out and page < 1:
        abort(404)

    items = query.skip((page - 1) * per_page).limit(per_page)

    if not items and page != 1 and err_out:
        abort(404)

    if page == 1 and items.count() < per_page:
        total = items.count()
    else:
        total = query.count()

    return Pagination(query, page, per_page, total, items)


class Pagination(object):
    """
    分页类 提供基本方法用于分页
    """

    def __init__(self, query, page, per_page, total, items):
        """
        构造函数
        :param query: 查询游标
        :param page: 当前页码
        :param per_page: 每页长度
        :param total: 总数
        :param items: 内容
        """
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        """
        总页数
        :return: int
        """
        if self.per_page == 0:
            return 0
        else:
            return int(ceil(self.total / float(self.per_page)))

    def prev(self, err_out=False):
        """
        返回上页的查询
        :param err_out:
        :return: Pagination
        """
        assert self.query is not None, 'this method needs a query object'
        return paginate(self.query, self.page - 1, self.per_page, err_out)

    @property
    def prev_num(self):
        """
        返回上一页的页号
        :return: int
        """
        return self.page - 1

    @property
    def has_prev(self):
        """
        返回是否有上一页
        :return: bool
        """
        return self.page > 1

    def next(self, err_out=False):
        """
        返回下页的查询
        :param err_out:
        :return: Pagination
        """
        assert self.query is not None, 'this method needs a query object'
        return paginate(self.query, self.page + 1, self.per_page, err_out)

    @property
    def next_num(self):
        """
        返回上一页的页号
        :return: int
        """
        return self.page + 1

    @property
    def has_next(self):
        """
        返回是否有上一页
        :return: bool
        """
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=4,
                   right_current=4, right_edge=2):
        """
        用于在模板中循环调用生成底部页面导航
        :param left_edge: 起始保留数
        :param left_current: 左侧数
        :param right_current: 右侧数
        :param right_edge: 末尾保留数
        :return: 按默认值为 "1, 2, ..., i-2, i-1, i, i+1, i+2, i+3, i+4, i+5, ..., n-1, n"
        """
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if (num <= left_edge or
                    (self.page - left_current - 1 < num < self.page + right_current) or
                    num > self.pages - right_edge):
                if last + 1 != num:
                    yield None
                yield num
                last = num


def rec_sum(id):
    item = mg.db.movie.find_one({'_id': id})
    genres_cursor = mg.db.movie.find({
        'genres': item['genres']
    }, RES_FILTER).limit(LIMIT)
    directors_cursor = mg.db.movie.find({
        'directors': item['directors']
    }, RES_FILTER).limit(LIMIT)
    writers_cursor = mg.db.movie.find({
        'writers': item['writers']
    }, RES_FILTER).limit(LIMIT)

    contents = []
    for i in xrange(2):
        cursor = mg.db.movie.find({'casts': {
            '$elemMatch': {
                'id': item['casts'][i]['id']
            }
        }}, RES_FILTER).limit(LIMIT)
        contents.extend(list(cursor))

    contents.extend(list(genres_cursor))
    contents.extend(list(directors_cursor))
    contents.extend(list(writers_cursor))

    rdd = recommender.sc.parallelize([x['_id'] for x in contents])
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
