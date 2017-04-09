# coding: utf-8
# Created by leo on 17-4-8.
"""
辅助工具
"""
import requests
from bs4 import BeautifulSoup


def add_douban_movie(id):
    """
    从豆瓣获取新电影
    :param id: subject id
    :return: dict
    """
    url = 'https://movie.douban.com/subject/'
    r = requests.get(url+id)
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