#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import sys
import xlwt
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")
wb = xlwt.Workbook(encoding='utf-8')
sheet1 = wb.add_sheet(u'1', cell_overwrite_ok=True)
sheet1.write(0,0,'fuck')

sheet2 = wb.add_sheet(u'2', cell_overwrite_ok=True)
sheet2.write(4,1,'fuck')
sheet2.write(1,1,'fuck')
sheet1.write(1,2,'duck')
wb.save('/Users/bjhl/Documents/yasi.xlsx')
#write(wb, self.order_map, self.res_dict, '全部数据')
dic = {'z': ''}
dic['z'] += 'a'
print dic