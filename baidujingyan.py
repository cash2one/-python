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
        #u'word', 'word.log',  ],
        #[u'日语', 'riyu.log',  ],
        #[u'职业规划', 'zhiyeguihua.log',  ],
        #[u'留学', 'liuxue.log',  ],
        #[u'新概念', 'xingainian.log',  ],
        #[u'大学', 'daxue.log',  ],
        # [u'photoshop', 'photoshop.log',  ],
        # [u'office', 'office.log',  ],
        # [u'求职', 'qiuzhi.log',  ],
        # [u'平面设计', 'pingmiansheji.log',  ],
        # [u'面试', 'mianshi.log',  ],
        # [u'教育', 'jiaoyu.log',  ],
        # #[u'高考', 'gaokao.log',  ],
        # [u'普通话', 'putonghua.log',  ],
        # [u'学习', 'xuexi.log',  ],
        # [u'编程语言', 'bianchengyuyan.log',  ],
        # [u'ASP', 'asp.log',  ],
        # [u'WORD', 'word.log',  ],
        # [u'水彩画', 'shuicaihua.log',  ],
        # [u'哲学', 'zhexue.log',  ],
        # [u'办公', 'bangong.log',  ],
        # [u'英语', 'yingyu.log',  ],
        # [u'招聘', 'zhaopin.log',  ],
        # [u'企业管理', 'qiyeguanli.log',  ],
        # [u'PS教程', 'psjiaocheng.log',  ],
        # [u'windows', 'windows.log',  ],
        # [u'企业经营', 'qiyeguanli.log',  ],
        # [u'高中生', 'gaozhongsheng.log',  ],
        # [u'考研', 'kaoyan.log',  ],
        # [u'网络', 'wangluo.log',  ],
        # [u'电脑软件', 'diannaoruanjian.log',  ],
        # [u'电脑技术', 'diannaojishu.log',  ],
        # [u'元素周期表', 'yuansuzhouqibiao.log',  ],
        # [u'PS', 'ps.log',  ],
        # [u'软件技巧', 'ruanjianjiqiao.log',  ],
        # [u'办公软件', 'bangongruanjian.log',  ],
        # [u'电脑技巧', 'diannaojiqiao.log',  ],
        # [u'中国象棋', 'zhongguoxiangqi.log',  ],
        # [u'移民', 'yiming.log',  ],
        # [u'dreamweaver', 'dreamweaver.log',  ],
        # [u'鼠标', 'shubiao.log',  ],
        # [u'WORDPRESS', 'wordpress.log',  ],
        # [u'windows7', 'windows7.log',  ],
        # [u'word2007', 'word2007.log',  ],
        # #[u'初中生', 'chuzhongsheng.log',  ],
        # #[u'笔记本', 'bijiben.log',  ],
        # [u'职场', 'zhichang.log',  ],
        # [u'ppt', 'ppt.log',  ],
        # [u'数学', 'shuxue.log',  ],
        # [u'物理', 'wuli.log',  ],
    ]

    #for url in [[u'物理', 'wuli.log', ],[u'数学', 'shuxue.log',  ],]:
    for url in deal_list:
        keyword = url[0]
        name = url[1]
        fw = open('/Users/bjhl/Documents/baidujinyan2/' + name, 'a')
        for i in range(0, 30000, 10):
            print i
            url = 'http://jingyan.baidu.com/tag?tagName=' + keyword + '&rn=10&pn=' + str(i)
            try:
                html = urllib2.urlopen(url).read()
                if '发布有何奖励' in html:
                    print keyword+'已爬完!'
                    break
                tree = etree.HTML(html)
                for node in tree.xpath("//a/@href"):
                    if 'article' in node:
                        if 'http' in node:
                            continue
                        fw.write(node + '\n')
                        fw.flush()
            except:
                traceback.print_exc()
                exit(1)
            time.sleep(2)
        fw.close()

get_article_url()