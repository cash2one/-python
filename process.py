#ecoding:utf-8
import os
import sys
import data
import json

reload(sys)
sys.setdefaultencoding("utf-8")


class Conf(object):
    def __init__(self, data):
        self.data = data

    def get_list(self, subject):
        res = {"list": {"retrieve": "size:10,offset:0,subject:%s"%subject, "tags": {}}}
        _dic = {}
        for index, items in enumerate(self.data):
            parent_id = index + 1
            for k, v in items.items():
                length = len(v)
                # print k, v
                _dic['%d'%parent_id] = {
                    "tag": k,
                    "name": k,
                }
                if not length:
                    continue
                _list = []
                for _index, _v in enumerate(v):
                    sub_id = _index + 1
                    _dic['%d_%d'%(parent_id, sub_id)] = {
                        "name": u'%s'%(_v[0]),
                        "tag": ",".join(_v)
                    }
                    _list.append(('%d'%sub_id))
                _dic['%d'%parent_id]["sub"] = ','.join(_list)
        res['list']['tags'] = _dic
        dict = {}
        dict['query'] = subject.split()[0]
        dict['name'] = "互动问答"
        dict['subject'] = "{domain_name} 问答"
        res['list']['tags']['100']=dict
        #print  res
        print json.dumps(res)

    def m_bread_button(self):
        res = {}
        for index, items in enumerate(self.data):
            parent_id = index + 1
            for k, v in items.items():
                length = len(v)
                if not length:
                    continue
                _list = []
                for _index, _v in enumerate(v):
                    sub_id = _index + 1
                    res['%d-%d'%(parent_id, sub_id)] = {
                        "url": "/a/%d/%d"%(parent_id, sub_id),
                        "parent_id": "%d"%parent_id,
                        "name": u'%s'%(_v[0]),
                        "id": "%d"%sub_id
                    }
                    _list.append(('%d-%d'%(parent_id, sub_id)))
                res['%d'%parent_id] = {"sub": ',pl,'.join(_list)}
        res["pl"] = {"pl": "1"}
        print json.dumps(res)

    def get_nav(self):
        res = {}
        nav_list = []
        for index, items in enumerate(self.data):
            parent_id = chr(index + 65)
            nav_list.append((parent_id))
            for k, v in items.items():
                res[parent_id] = {
                    "name": u'%s'%k,
                    "id": '%d'%(index + 1),
                    "url": '/a/%d/'%(index + 1),
                }
                length = len(v)
                if length:
                    _list = []
                    for _index, _v in enumerate(v):
                        sub_id = chr(_index + 65)
                        res['%s_sub_%s'%(parent_id, sub_id)] = {
                            "url": "/a/%d/%d/"%(index + 1, _index + 1),
                            "name": u'%s'%(_v[0]),
                        }
                        _list.append((sub_id))
                        res['%s_sub'%parent_id] = {'tab': ','.join(_list)}
                        res[parent_id]['sub'] = '%s_sub'%(parent_id)

        # res['base'] = {'tab': ','.join(nav_list)}
        # 添加问答
        res['Y'] = {"url":"/a/100/","name":"互动问答","id":"100"}
        res['Z'] = {"url":"/course/","sub":"Z_sub","id":"course","name":"课程资源"}
        res['Z_sub'] = {"tab":"A,B"}
        res['Z_sub_A'] = {"url":"/course/2","name":"在线直播"}
        res['Z_sub_B'] = {"url":"/course/3","name":"视频课程"}
        nav_list.append('Y')
        nav_list.insert(2,'Z')
       # print  nav_list
        res['base'] = {'tab': ','.join(nav_list)}
        print json.dumps(res)

if __name__ == '__main__':
    conf = Conf(data.sheji)
    conf.m_bread_button()
    conf.get_list("鼓 非百站新闻")
    conf.get_nav()