# -*- coding: utf-8 -*-
import os
import requests
from lxml import html

headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}
def save(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    filepath = os.path.join('image', filename)
    with open(filepath, 'w') as f:
        print '正在保存' + filepath
        f.write(page)

def crawl(url):
    resp = requests.get(url, headers=headers)
    page = resp.content
    root = html.fromstring(page)
    image_urls = root.xpath('//img[@data-original]/@data-original')
    for image_url in image_urls:
        save(image_url)

if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/27364360' 
    crawl(url)