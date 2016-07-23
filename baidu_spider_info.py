# _*_ coding: utf-8 _*_
import os
import re
import sys
import datetime
import json
import urlparse
import hashlib
import traceback
from collections import defaultdict
import MySQLdb
#from util.DBFactory import factory

#db_util = factory.get_db('online')
conn = MySQLdb.connect(host="drds1pouikzz3j49.drds.aliyuncs.com",user="db_statistics",passwd="mNKb4uv2zV91wrRw",port=3306, db="db_statistics")

__author__ = 'Zhihao Xu <xuzhihao@baijiahulian.com>'
__version__ = "1.0.0"
__date__ = "16/06/21"
spiders_dic = {'baidu': 'Baiduspider',
               'sougou': 'Sogou web spider',
               'sm': 'YisouSpider',
               '360': '360Spider',}
folders_dic = {'www': '/apps/log/nginx/www.genshuixue.com',
               'm': '/apps/log/nginx/m.genshuixue.com',}
#object=day
class ActiveLogHour(object):
    def __init__(self, day):
        self.day = day
        self.date = datetime.datetime.strptime(day, '%Y%m%d').strftime("%Y-%m-%d")
        self.records = []
        self.chinese_dic, self.en_dic = self.get_baizhan_dic()

    def get_url_type(self, k):
        if 'robots.txt' in k or 'xml' in k or '/captcha' in k:
            url_type = 'other'
        elif k == '/':
            url_type = 'index'
        elif '/i-' in k:
            if '/p/' in k:
                url_type = 'zhanqun_detail'
            elif '/a/' in k:
                url_type = 'zhanqun_subject'
            else:
                url_type = 'zhanqun'
        elif '/sc' in k:
            url_type = 'sc'
        elif '/st' in k:
            url_type = 'st'
        elif '/so' in k:
            url_type = 'so'
        elif 'tiku' in k:
            if '.html' in k:
                url_type = 'tuku_detail'
            elif 'tiku/s_' in k:
                url_type = 'tiku_subject'
            elif 'tiku/p_' in k:
                url_type = 'tiku_point'
            else:
                url_type = 'tiku'
        elif 'wenda' in k:
            if '.html' in k:
                url_type = 'wenda_detail'
            else:
                url_type = 'wenda'
        elif '/i/' in k or '/org/' in k:
            url_type = 'org'
        elif '/x/' in k:
            url_type = 'x'
        elif 'one2oneCourseDetail' in k:
            url_type = 'one2oneCourseDetail'
        elif 'classCourseDetail' in k:
            url_type = 'classCourseDetail'
        elif 'video_course' in k:
            url_type = 'video_course'
        elif 'org_class_course' in k:
            url_type = 'org_class_course'
        elif '/letter/' in k:
            url_type = 'letter'
        else:
            url_type = 'other'
        return url_type

    def get_baizhan_dic(self):
        chinese_dic, en_dic = {}, {}
        with open('/apps3/rd/xuzhihao/dim_baizhan_site') as f:
            for line in f:
                (chinese, en) = line.strip('\n').split()
                chinese_dic[chinese] = en.lower()
                en_dic[en.lower()] = chinese
        return chinese_dic, en_dic

    def process_records(self, folder):
        res_dic = {}
        for i in range(24):
            dst_folder = '%s/%s/%.2d'%(folder, self.day, i)
            try:
                for file in os.listdir(dst_folder):
                    src_file = '%s/%s'%(dst_folder, file)
                    with open(src_file) as f:
                        for line in f:
                            data = line.strip('\n').split('\x01')
                            request_url = data[3]
                            refer_url = data[9]
                            for spider, spider_type in spiders_dic.iteritems():
                                if spider_type in refer_url: #and 'spider' in refer_url:
                                    if spider not in res_dic:
                                        res_dic[spider] = defaultdict(int)
                                    k = request_url.split()[1].split('?')[0]
                                    if 'tiku' in k:
                                        print k
                                    url_type = self.get_url_type(k)
                                    res_dic[spider][url_type] += 1
                                    break
            except:
                traceback.print_exc()
        return res_dic

    def run(self):
        cursor = conn.cursor()
        #fo = open('spiderlog.txt', 'a')
        for site, folder in folders_dic.iteritems():
            res_dic = self.process_records(folder)
            print site
            for spider_type, dic in res_dic.iteritems():
                print spider_type
                for k, v in dic.iteritems():
                    sql = """
                        insert into habo_seo_spider (terminal, source, url_type, pv, create_date) values ('%s', '%s',
                        '%s', %d, '%s') on duplicate key update pv=values(pv)
                    """%(site, spider_type, k, v, self.date)
                    #print sql
                    #fo.write(str(site) +' '+str(spider_type) +' '+str(k) +' '+str(v) +' '+str(self.date) +'\n')
                    #db_util.stat(sql)
                    cursor.execute(sql)
        conn.commit()
        conn.close()
        #fo.close()

if __name__ == "__main__":
    usage = 'usage: python %s [date]\n' % (__file__)
    if len(sys.argv) == 2:
        which_day = sys.argv[1]
    else:
        which_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    ActiveLogHour(which_day).run()