#coding=utf-8
import requests
import codecs
from pyquery import PyQuery as pq
import sys
import time
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf8')


def new_md(date, filename):
    with open(filename, 'w') as f:
        f.write('## {date}\n\n'.format(date=date))


def deploy_git(date):
    os.system('git add .')
    os.system('git commit -m "{date}"'.format(date=date))
    os.system('git push -u origin master')


def get_trending(lang, filename):
    HEADERS = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':
        'gzip,deflate,sdch',
        'Accept-Language':
        'zh-CN,zh;q=0.8'
    }
    res = requests.get(
        'https://github.com/trending?l={lang}'.format(lang=lang),
        headers=HEADERS)
    d = pq(res.content)
    items = d('ol.repo-list li')

    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n## {lang}\n'.format(lang=lang))
        f.write('项目 | 描述 \n ---|---\n')
        for item in items:
            i = pq(item)
            title = i("h3 a").text()
            owner = i("span.text-normal").text()
            description = i("p.col-9").text()
            url = "https://github.com" + i("h3 a").attr("href")
            line = "[{title}]({url}) | {description} \n".format(
                title=title, url=url, description=description, owner=owner)
            f.write(line)


def start():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = strdate + '.md'
    new_md(strdate, filename)

    list = ['javascript', 'python', 'vue', 'c', 'typescript']
    for l in list:
        get_trending(l, filename)
    deploy_git(strdate)


if __name__ == '__main__':

    while True:
        start()
        time.sleep(24 * 60 * 60)