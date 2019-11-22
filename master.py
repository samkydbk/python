#coding:utf-8
import requests
import re
import math
import sys
import redis
import traceback
from bs4 import BeautifulSoup
from pymongo import MongoClient
from multiprocessing.pool import ThreadPool
#电影详细数据
dy_data = []
#分页条数
limit = 50
#网站网址
website = 'http://www.zuidazy1.net'
#抓取的网站地址
url = website + '/index.php?m=vod-search'
#需要抓取的列表页
url_list = []
#搜索获取电影详情页
search_url = website + '/index.php?m=vod-search-pg-%d-wd-%s.html'

#爬取指定电影关键词入口
def crawl():
    name = input('输入想看的电影: ')
    params = {
        'wd': name,
        'submit': "search",
    }
    res = requests.post(url, params)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    #获取指定关键词搜索分页数据结果
    pagenum = soup.find_all('div', class_='pages')[0].get_text()
    #获取搜索结果总数
    total = re.match('共(\d*)', pagenum)
    if total is not None:
        total = total.groups()[0]
    #总分页数量 总数量/分页大小向上取整
    page = math.ceil(int(total) / int(limit)) + 1
    #构建列表页url
    #http://www.zuidazy1.net/index.php?m=vod-search-pg-2-wd-1234.html
    url_list = [search_url % (int(i), name) for i in range(1, page)]
    pool = ThreadPool(2)
    pool.map(list_page_thread, url_list[:2])
    pool.close()
    pool.join()

#爬取电影列表页数据
def list_page_thread(url):
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        'accept': "application/json",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'accept-encoding': "gzip, deflate, br",
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    for i in soup.find('div', class_='xing_vb').find_all('li'):
        if i.find('a') is not None:
            content_url = website + i.find('a').get('href')
            #爬取详情页
            content(content_url)

#爬取电影详情页
def content(url):
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        'accept': "application/json",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'accept-encoding': "gzip, deflate, br",
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    dy_data = {}
    #影片名称
    dy_data['title'] = soup.find('h2').text
    #影片类型
    dy_data['type'] = soup.find('div', class_='vodinfobox').find_all('li')[3].find('span').text
    #影片地区
    dy_data['region'] = soup.find('div', class_='vodinfobox').find_all('li')[4].find('span').text
    #影片简介
    dy_data['story'] = soup.find('div', class_='jjText').find('span', class_='more').text
    #播放地址
    if soup.find('div', id='play_2') is not None:
        dy_data['play_url'] = soup.find('div', id='play_2').find_all('input')[0].get('value')
    #下载地址
    if soup.find('div', id='down_1') is not None:
        dy_data['download_url'] = soup.find('div', id='down_1').find_all('input')[0].get('value')
    #数据存储到mongodb
    saveData(dy_data)

#数据写入mongodb
def saveData(data):
    #连接mongodb数据库
    client = MongoClient('mongodb://localhost:27017/')
    # 连接mydb数据库,账号密码认证。先连接系统默认数据库admin
    db = client.admin
    #让admin数据库去认证密码登录
    db.authenticate("root", "root")
    #获取电影数据库test
    my_db = client.test
    #获取集合不存在创建集合
    collection = my_db.movie
    #写入mongodb数据
    try:
        collection.insert_one(data)
    except Exception:
        traceback.print_exc()

crawl()