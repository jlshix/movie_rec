# coding: utf-8
# Created by leo on 17-4-19.
import requests
from bs4 import BeautifulSoup

r = requests.get('https://movie.douban.com/tag/')
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find('table', class_='tagCol')
tags = table.find_all('a')
# for tag in tags:
#     print tag.get_text()

tlist = [t.get_text() for t in tags]
print '", "'.join(tlist)
