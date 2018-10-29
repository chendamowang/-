# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from lxml import html
import MySQLdb
import multiprocessing


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
}


def crawl(url):
    resp = requests.get(url, headers=headers)
    con = resp.content
    root = html.fromstring(con)
    info = root.xpath('//div[@class="info"]')
    for i in info:
        #电影名字
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]

        #年代、国家、类型
        small_info = i.xpath('div[@class="bd"]/p/text()')[1]
        year = small_info.replace("\n", "").replace(" ", "").split("/")[0]
        country = small_info.replace("\n", "").replace(" ", "").split("/")[1]
        type = small_info.replace("\n", "").replace(" ", "").split("/")[2]

        #电影评分
        score = i.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]

        print title, score, year, country, type
        #存入数据库
        db.execute("insert into movie (m_title,m_score,m_year,m_country,m_type) values (%s,%s,%s,%s,%s)",
                   (title, score, year, country, type))
        conn.commit()

if __name__=='__main__':
    #连接数据库
    print '连接数据库'
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123", db="douban", charset="utf8")
    db = conn.cursor()
    print '数据库连接成功'

    #url集合
    urls = set()
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        urls.add(url)

    #多进程
    p = multiprocessing.Pool()
    for url in urls:
        p.apply_async(crawl, args=(url,))
    p.close()
    p.join()

    db.close()
    conn.close()
    print 'done!'