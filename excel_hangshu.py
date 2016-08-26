#ecoding:utf-8
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")

import os
count = 0
for f in os.listdir(u'/Users/bjhl/Documents/小学库/已编完/'):
    if f.endswith('.xlsx'):
        data = xlrd.open_workbook(u'/Users/bjhl/Documents/小学库/已编完/'+f)
        table = data.sheets()[0]
        nrows = table.nrows #行数
        count += nrows
print count
