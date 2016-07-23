#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import sys, os
import MySQLdb
import traceback
from zhanqun_statistic import ZhanQun

__author__ = 'xuzhihao <xuzhihao@baijiahulian.com>'
__version__ = "1.0.0"
__date__ = "16/2/17"

conn = MySQLdb.connect(host="drdse7h0fv7cmp68.drds.aliyuncs.com",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun",charset="utf8")

def process(day, date):
    #dst_file = './%s.log'%day
    #os.system('hdfs dfs -get /ad/zhanqun/database/corpora/temp/%s_tongji/part-00000 %s'%(day, dst_file))
    dst_file = '/apps3/rd/yangxiaoyun/zhanqun/online/jobs/tongji/data/%s/part-00000'%(day)
    cursor = conn.cursor()
    for line in open(dst_file):
        try:
            (site, num) = line.strip('\n').split('\t')
            sql = """
                insert into baizhan_site_info (site, num, `date`) values ('%s', %d, '%s')
                on duplicate key update num=values(num)
            """ % (site, int(num), date)
            cursor.execute(sql)
            conn.commit()
        except:
            traceback.print_exc()

if __name__ == '__main__':
    day = datetime.datetime.now().strftime("%Y%m%d")
    date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    process(day, date)
    ZhanQun(datetime.datetime.now() - datetime.timedelta(days=1)).run()