#ecoding:utf-8
import json
import traceback
import sys
import datetime
import urllib2, urllib
import urlparse
#from pyquery import PyQuery
from lxml import etree
import time
import random
#import requests
import webbrowser
import os
#os.putenv('http_proxy', '119.188.94.145:80')
#proxies = {'http': '119.188.94.145:80'}

reload(sys)
sys.setdefaultencoding("utf-8")

def get_article_url():
    deal_list = [
        #['高考', 'gaokao.log', 2181],
        # ['留学', 'liuxue.log', 1261],
        # ['考研', 'kaoyan.log', 1061],
        # ['公务员', 'gongwuyuan.log', 1031],
        # [u'中考', 'zhognkao.log', 471]
        #[u'励志', 'lizhi.log',  ],
        #[u'试用期', 'shiyongqi.log',  ],
        #[u'校园生活', 'xiaoyuanshenghuo.log',  ],
        #[u'转正', 'zhuanzheng.log',  ],
        #[u'离职', 'lizhi2.log',  ],
        #[u'GRE', 'gre.log',  ],
        #[u'简历', 'jianli.log',  ],
        #[u'抠图', 'koutu.log',  ],
        #[u'学校', 'xuexiao.log',  ],
        #[u'兼职', 'jianzhi.log',  ],
        #[u'古籍', 'guji.log',  ],
        [u'word', 'word.log',  ],
        [u'日语', 'riyu.log',  ],
        [u'职业规划', 'zhiyeguihua.log',  ],
        [u'留学', 'liuxue.log',  ],
        [u'新概念', 'xingainian.log',  ],
        [u'大学', 'daxue.log',  ],
        [u'photoshop', 'photoshop.log',  ],
        [u'office', 'office.log',  ],
        [u'求职', 'qiuzhi.log',  ],
        [u'平面设计', 'pingmiansheji.log',  ],
        [u'面试', 'mianshi.log',  ],
        [u'教育', 'jiaoyu.log',  ],
        #[u'高考', 'gaokao.log',  ],
        [u'普通话', 'putonghua.log',  ],
        [u'学习', 'xuexi.log',  ],
        [u'编程语言', 'bianchengyuyan.log',  ],
        [u'ASP', 'asp.log',  ],
        [u'WORD', 'word.log',  ],
        [u'水彩画', 'shuicaihua.log',  ],
        [u'哲学', 'zhexue.log',  ],
        [u'办公', 'bangong.log',  ],
        [u'英语', 'yingyu.log',  ],
        [u'招聘', 'zhaopin.log',  ],
        [u'企业管理', 'qiyeguanli.log',  ],
        [u'PS教程', 'psjiaocheng.log',  ],
        [u'windows', 'windows.log',  ],
        [u'企业经营', 'qiyeguanli.log',  ],
        [u'高中生', 'gaozhongsheng.log',  ],
        [u'考研', 'kaoyan.log',  ],
        [u'网络', 'wangluo.log',  ],
        [u'电脑软件', 'diannaoruanjian.log',  ],
        [u'电脑技术', 'diannaojishu.log',  ],
        [u'元素周期表', 'yuansuzhouqibiao.log',  ],
        [u'PS', 'ps.log',  ],
        [u'软件技巧', 'ruanjianjiqiao.log',  ],
        [u'办公软件', 'bangongruanjian.log',  ],
        [u'电脑技巧', 'diannaojiqiao.log',  ],
        [u'中国象棋', 'zhongguoxiangqi.log',  ],
        [u'移民', 'yiming.log',  ],
        [u'dreamweaver', 'dreamweaver.log',  ],
        [u'鼠标', 'shubiao.log',  ],
        [u'WORDPRESS', 'wordpress.log',  ],
        [u'windows7', 'windows7.log',  ],
        [u'word2007', 'word2007.log',  ],
        [u'初中生', 'chuzhongsheng.log',  ],
        [u'笔记本', 'bijiben.log',  ],
        [u'职场', 'zhichang.log',  ],
        [u'ppt', 'ppt.log',  ],
        [u'数学', 'shuxue.log',  ],
        [u'物理', 'wuli.log',  ],
    ]
    urls = [
        'http://jingyan.baidu.com/',
        'http://jingyan.baidu.com/article/f79b7cb34690499144023ea9.html',
        'http://jingyan.baidu.com/article/2f9b480d49fdea41ca6cc275.html',
        'http://jingyan.baidu.com/z/201607food.html',
        'http://jingyan.baidu.com/article/fec7a1e513fd571190b4e7af.html',
    ]
    i = 0
    index = 0
    while 1:
    #for i in range(0,100000):
        print i
        i += 1
            #import webbrowser
            #webbrowser.open("http://jingyan.baidu.com/")
            #urllib2.urlopen(url)
            #print html
        try:
            if index == 3:
                index = 0
            webbrowser.open(urls[index])
            index += 1
            #urllib2.urlopen(url)
            # url = "http://jingyan.baidu.com/"
            # req_header = {
            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            #     'Accept': '*/*',
            #     'Accept-Encoding': 'gzip, deflate, sdch',
            #     'Connection': 'keep-alive',
            #     'Referer': 'http://jingyan.baidu.com/',  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
            #     'Accept - Language':'zh - CN, zh;q = 0.8',
            #     'Cache - Control':'max - age = 0',
            #     'Connection':'keep - alive',
            #     'Cookie':'BIDUPSID=95758806E23E59F77C5DF4F33190F684; PSTM=1465965337; bdshare_firstime=1465965355205; BDUSS=TFBdlNZTzZRd3ZCQ2w0ZmtCS1F0T3pDajA2LXRyaTE5anI2Y0FyV0tZWDlvNGhYQUFBQUFBJCQAAAAAAAAAAAEAAACuY~2QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP0WYVf9FmFXZ; isStepGuided=done; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1454_20515_20536_17942_20539_20415_20455_18559_15541_12247_19790; Hm_lvt_46c8852ae89f7d9526f0082fafa15edd=1467627144,1467627210,1467628343,1467629051; Hm_lpvt_46c8852ae89f7d9526f0082fafa15edd=1467687647;',
            #     'Host':'jingyan.baidu.com',
            #     'Referer':'http: // jingyan.baidu.com /',
            #     'X - Requested - With':'XMLHttpRequest',
            #     }
            # req_timeout = 5
            # req = urllib2.Request(url, None, req_header)
            # urllib2.urlopen(req, None, req_timeout)
        except:
            traceback.print_exc()
            continue

        time.sleep(4)




get_article_url()