# _*_ coding: utf-8 _*_
import traceback
import sys
import os
import re
import datetime
from util.log_generator import BaseLogDataHourGenerator
from itertools import groupby
from collections import Counter
from operator import itemgetter
from util.SequenceNumber import SequenceNumber
from collections import defaultdict
import MySQLdb
import urllib
import xlwt

__author__ = 'Zhihao Xu <xuzhihao@baijiahulian.com>'
__version__ = "1.0.0"
__date__ = "15/12/11"

reload(sys)
sys.setdefaultencoding("utf-8")

conn = MySQLdb.connect(host="drdse7h0fv7cmp68.drds.aliyuncs.com", user="zhanqun", passwd="wdlPD40xjO5", db="zhanqun",
                       charset="utf8")

folders_dic = {'base_log_data': '/apps2/log/base_log_data/',}
key_word = '钢琴'
key_url = '/i-gangqin/'
search_word = '/s/'
xls_name = 'gangqin.xls'
type_class = ['46', '3']

class ZhanQun(object):
    def __init__(self, date):
        self.date = date
        self.date_time = self.date.strftime("%Y-%m-%d")
        self.day = self.date.strftime("%Y%m%d")
        self.id_dict = self.get_id_subject_dic()
        self.baizhan_china_dic = self.get_baizhan_dic()
        self.baizhan_en_dic = {v: k for k, v in self.baizhan_china_dic.iteritems()}
        self.school_dict = {}
        self.dic = {}
        self.zhandian_dic = {}

    def get_baizhan_dic(self):
        dic = {}
        with open('/apps3/rd/xuzhihao/dim_baizhan_site') as f:
            for line in f:
                (chinese, en) = line.strip('\n').split()
                dic[chinese] = en
        return dic

    def get_id_subject_dic(self):
        dic = {}
        with open('/apps3/rd/xuzhihao/zhanqun_id_infos') as f:
            for line in f:
                (id, _class, subject, subject_1, subject_2) = line.strip('\n').split('\x01')
                dic[id] = [_class, subject, subject_1]
        # print dic
        return dic

    def get_records(self, folder, index_day):
        res_list = []
        #dst_folder = '%s/%s' % (folder, self.day)
        dst_folder = '%s/%s' % (folder, (self.date - datetime.timedelta(days=index_day)).strftime("%Y%m%d"))
        index_day -= 1
        try:
            for file in os.listdir(dst_folder):
                src_file = '%s/%s' % (dst_folder, file)
                with open(src_file) as f:
                    for line in f:
                        data = line.strip('\n').split('\x01')
                        if '/i-' in data[5]:
                            res_list.append({'request_url': data[5], 'new_session_id': data[21], 'page_type': data[24]})
        except:
            traceback.print_exc()
        # print res_list[:20]
        return res_list

    def run(self):
        for site, folder in folders_dic.iteritems():
            index_day = 7
            wb = xlwt.Workbook(encoding='utf-8')
            sheet1 = wb.add_sheet(u'subject', cell_overwrite_ok=True)
            sheet2 = wb.add_sheet(u'keyword', cell_overwrite_ok=True)
            sheet3 = wb.add_sheet(u'detail', cell_overwrite_ok=True)
            sheet4 = wb.add_sheet(u'other', cell_overwrite_ok=True)
            while index_day > 0:
                records = self.get_records(folder, index_day)
                self.process_records(records, index_day, sheet1, sheet2, sheet3, sheet4)
                index_day -= 1
                # self.data_inset()
            wb.save(xls_name)

    def process_records(self, records, index_day, sheet1, sheet2, sheet3, sheet4):
        # for url_type in subject_dic.itervalues():
        #     self.zhandian_dic["列表\x01" + str(url_type)] = {'pv': 0, 'uv': set()}
        for record in records:
            request_url = urllib.unquote(record['request_url']).decode('utf-8', 'replace')
            new_session_id = record['new_session_id']
            page_type = record['page_type']

            detail_id = request_url.split('?')[0].split('/')[-1]
            request_url = request_url.split('?')[0]
            if detail_id.isdigit() and detail_id in self.id_dict:
                if detail_id not in self.dic and key_word in self.id_dict[detail_id][1]:
                    self.dic[detail_id] = {'pv': 0, 'uv': set()}
                    self.dic[detail_id]['pv'] += 1
                    self.dic[detail_id]['uv'].add(new_session_id)
                    if self.id_dict[detail_id][0] == type_class[0] and "详情\x01" + key_word + type_class[0] not in self.zhandian_dic:
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]] = {'pv': 0, 'uv': set()}
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['pv'] += 1
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['uv'].add(new_session_id)
                    elif self.id_dict[detail_id][0] == type_class[1] and "详情\x01" + key_word + type_class[1] not in self.zhandian_dic:
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]] = {'pv': 0, 'uv': set()}
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['pv'] += 1
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['uv'].add(new_session_id)
                elif detail_id in self.dic and key_word in self.id_dict[detail_id][1]:
                    self.dic[detail_id]['pv'] += 1
                    self.dic[detail_id]['uv'].add(new_session_id)
                    if self.id_dict[detail_id][0] == type_class[0]:
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['pv'] += 1
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['uv'].add(new_session_id)
                    elif self.id_dict[detail_id][0] == type_class[1]:
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['pv'] += 1
                        self.zhandian_dic["详情\x01" + key_word + self.id_dict[detail_id][0]]['uv'].add(new_session_id)
            elif key_url in request_url:
                if '/a/' in request_url:
                    url_type = "列表\x01" + request_url
                    if url_type not in self.zhandian_dic:
                        self.zhandian_dic[url_type] = {'pv': 0, 'uv': set()}
                    self.zhandian_dic[url_type]['pv'] += 1
                    self.zhandian_dic[url_type]['uv'].add(new_session_id)
                elif search_word in request_url:
                    url_type = '关键字\x01' + request_url.split('/')[5]
                    if url_type not in self.zhandian_dic:
                        self.zhandian_dic[url_type] = {'pv': 0, 'uv': set()}
                    self.zhandian_dic[url_type]['pv'] += 1
                    self.zhandian_dic[url_type]['uv'].add(new_session_id)
                else:
                    url_type = request_url
                    if url_type not in self.zhandian_dic:
                        self.zhandian_dic[url_type] = {'pv': 0, 'uv': set()}
                    self.zhandian_dic[url_type]['pv'] += 1
                    self.zhandian_dic[url_type]['uv'].add(new_session_id)


        r_s, c_s = 1, (7-index_day) * 3
        r_k, c_k = 1, (7-index_day) * 3
        r_d, c_d = 1, (7-index_day) * 3
        r_o, c_o = 1, (7-index_day) * 3
        sheet1.write(0, (7-index_day) * 3+0, (self.date - datetime.timedelta(days=index_day)).strftime("%Y%m%d"))
        sheet1.write(0, (7-index_day) * 3+1, 'pv')
        sheet1.write(0, (7-index_day) * 3+2, 'uv')
        sheet2.write(0, (7-index_day) * 3+0, (self.date - datetime.timedelta(days=index_day)).strftime("%Y%m%d"))
        sheet2.write(0, (7-index_day) * 3+1, 'pv')
        sheet2.write(0, (7-index_day) * 3+2, 'uv')
        sheet3.write(0, (7-index_day) * 3+0, (self.date - datetime.timedelta(days=index_day)).strftime("%Y%m%d"))
        sheet3.write(0, (7-index_day) * 3+1, 'pv')
        sheet3.write(0, (7-index_day) * 3+2, 'uv')
        sheet4.write(0, (7-index_day) * 3+0, (self.date - datetime.timedelta(days=index_day)).strftime("%Y%m%d"))
        sheet4.write(0, (7-index_day) * 3+1, 'pv')
        sheet4.write(0, (7-index_day) * 3+2, 'uv')
        for k, v in self.zhandian_dic.iteritems():
            if '列表\x01' in k:
                sheet1.write(r_s, c_s, str(k).strip().split('\x01')[1])
                c_s += 1
                sheet1.write(r_s, c_s, int(v['pv']))
                c_s += 1
                sheet1.write(r_s, c_s, len(v['uv']))
                c_s = (7-index_day) * 3
                r_s += 1
            elif '关键字\x01' in k:
                sheet2.write(r_k, c_k, str(k).strip().split('\x01')[1])
                c_k += 1
                sheet2.write(r_k, c_k, int(v['pv']))
                c_k += 1
                sheet2.write(r_k, c_k, len(v['uv']))
                c_k = (7-index_day) * 3
                r_k += 1
            elif '详情\x01' in k:
                sheet3.write(r_d, c_d, str(k).strip().split('\x01')[1])
                c_d += 1
                sheet3.write(r_d, c_d, int(v['pv']))
                c_d += 1
                sheet3.write(r_d, c_d, len(v['uv']))
                c_d = (7-index_day) * 3
                r_d += 1
            else:
                sheet4.write(r_o, c_o, str(k))
                c_o += 1
                sheet4.write(r_o, c_o, int(v['pv']))
                c_o += 1
                sheet4.write(r_o, c_o, len(v['uv']))
                c_o = (7-index_day) * 3
                r_o += 1
        self.dic = {}
        self.zhandian_dic = {}




def fix():
    start_time = datetime.datetime(2016, 06, 02)
    end_time = datetime.datetime(2016, 05, 01)
    while start_time >= end_time:
        # which_day = start_time.strftime("%Y-%m-%d")
        print 'which_day:', start_time
        ZhanQun(start_time).run()
        start_time += datetime.timedelta(days=-1)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        which_day = sys.argv[1]
        _date = datetime.datetime.strptime("%s %s" % (which_day, '23'), "%Y-%m-%d %H")
    else:
        _date = datetime.datetime.now()
    ZhanQun(_date).run()
