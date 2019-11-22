#coding:utf-8
import traceback
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys

html = """
<div class="xing_vb"> 
   <ul>
    <li><span class="xing_vb1">影片名称</span><span class="xing_vb2">影片类别</span><span class="xing_vb3">更新时间</span></li>
   </ul>
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-70341.html" target="_blank">现代爱情第一季<span>8集全</span></a></span> <span class="xing_vb5">欧美剧</span> <span class="xing_vb6">2019-10-18</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63051.html" target="_blank">模范欲妻<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-11</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63160.html" target="_blank">波多野结衣之欲乱上班族<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-10</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-67641.html" target="_blank">上流赤裸复仇<span> 中文字幕</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-09</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63158.html" target="_blank">波多野结衣之潜藏淫欲<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-08</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63093.html" target="_blank">波多野结衣之裸话情缘<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-08</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63159.html" target="_blank">波多野结衣人妻奴隶<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-08</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-63144.html" target="_blank">柏青哥女王波多野结衣<span>BD高清中字</span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2019-09-08</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-10111.html" target="_blank">新木乃伊<span>HD1280高清中英双字版</span></a></span> <span class="xing_vb5">动作片</span> <span class="xing_vb6">2019-09-06</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-45921.html" target="_blank">波多黎各人在巴黎<span>BD高清中字</span></a></span> <span class="xing_vb5">喜剧片</span> <span class="xing_vb6">2019-03-18</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-57130.html" target="_blank">高潮2018<span>BD1280高清中字版</span></a></span> <span class="xing_vb5">恐怖片</span> <span class="xing_vb6">2019-02-28</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-53534.html" target="_blank">阿尔忒弥斯酒店<span>BD1280高清中英双字版</span></a></span> <span class="xing_vb5">动作片</span> <span class="xing_vb6">2018-10-05</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-50925.html" target="_blank">怪兽：黑暗大陆<span>BD1280高清中英双字版</span></a></span> <span class="xing_vb5">科幻片</span> <span class="xing_vb6">2018-07-21</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-41000.html" target="_blank">沙西米<span></span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2017-10-20</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-40901.html" target="_blank">王牌特工：特工学院<span>BD1280高清原声|国语中英双字版</span></a></span> <span class="xing_vb5">动作片</span> <span class="xing_vb6">2017-10-17</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-33100.html" target="_blank">守望人妻<span></span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2017-07-12</span></li>
   </ul> 
    
   <ul>
    <li><span class="tt"></span><span class="xing_vb4"><a href="/?m=vod-detail-id-36698.html" target="_blank">3D豪情<span></span></a></span> <span class="xing_vb5">伦理片</span> <span class="xing_vb6">2017-06-16</span></li>
   </ul> 
    
   <ul style="display:block;clear:both;">
    <li>
     <div class="pages" style="margin-bottom:10px;">共17条数据&nbsp;当前:1/1页&nbsp;<em>首页</em>&nbsp;<em>上一页</em>&nbsp;<span class="pagenow">1</span>&nbsp;<em>下一页</em>&nbsp;<em>尾页</em>&nbsp;<input type="input" name="page" id="page" size="4" class="pagego"><input type="button" value="跳 转" onclick="pagego('/index.php?m=vod-search-pg-{pg}-wd-%E6%B3%A2%E5%A4%9A.html',1)" class="pagebtn"></div></li>
   </ul> 
   <div style="clear:both"></div> 
  </div>
"""
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


soup = BeautifulSoup(html, 'lxml')

for i in soup.find('div', class_='xing_vb').find_all('li'):
    if i.find('a') is not None:
        content_url = 'http://www.zuidazy1.net' + i.find('a').get('href')
        data = {
            'url':content_url
        }
        saveData(data)
        sys.exit()

