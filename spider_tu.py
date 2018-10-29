
# -*- coding: utf-8 -*-
import os
import requests
from lxml import html
import time
import multiprocessing

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer':'http://i.meizitu.net'
}


def save(pic_urls, title):
    path = '[%dp]%s' % (len(pic_urls), title)
    os.mkdir(path)
    k = 1
    for pic_url in pic_urls:
        filepath = path+'/'+'%d.jpg'%k
        with open(filepath, 'w') as f:
            print 'output: %s' % (filepath)
            f.write(requests.get(pic_url, headers=headers).content)
            time.sleep(0.5)
        k += 1

def piclink(url):
    resp = requests.get(url)
    page = resp.content
    subroot = html.fromstring(page)
    title = subroot.xpath('//h2[@class="main-title"]/text()')[0]
    num = int(subroot.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0])
    pic_urls = set()
    for i in range(num):
        page_url = url+'/'+ str(i+1)
        r = requests.get(page_url)
        im = html.fromstring(r.content)
        pic_url = im.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        pic_urls.add(pic_url)

    save(pic_urls, title)


def crawl(url):
    resp = requests.get(url)
    page = resp.content
    root = html.fromstring(page)
    urls = root.xpath('//ul[@id="pins"]/li/a/@href')

    return urls


if __name__ == '__main__':
    page = raw_input('页码')
    url = 'http://www.mzitu.com/hot/page/%s' % page
    start = time.time()
    urls = crawl(url)
    p = multiprocessing.Pool()
    for url in urls:
        p.apply_async(piclink, args=(url,))
    p.close()
    p.join()
    end = time.time()
    a = end -start
    print 'done'
    print a
