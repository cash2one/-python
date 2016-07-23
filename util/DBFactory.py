#!/usr/bin/python
# -*- coding: utf-8 -*-
from util.HiveUtil import HiveUtil
from util.Properties import Properties
from 跟谁学.util.DBUtil import DBUtil

__author__ = 'Will Wang <wangweiwei@baijiahulian.com>'
__version__ = "1.0.0"
__date__ = "15/3/26"


class DBFactory(object):
    def __init__(self):
        self.dbs = {}
        import os

        home = os.getenv('HOME')
        pro = Properties(home + '/habo/etl/python/resources/db.properties')
        self.property = pro.get_properties()

    def get_db(self, name):
        """
        :rtype: DBUtil
        """
        if name in self.dbs:
            return self.dbs[name]
        else:
            if name == 'hive':
                self.dbs[name] = HiveUtil()
                return self.dbs[name]
            try:
                charset = self.property[name + '.charset']
            except KeyError:
                charset = 'utf8'
                pass
            # 读取数据使用RDS
            read_conf = {
                'host': self.property[name + '.host'],
                'user': self.property[name + '.user'],
                'passwd': self.property[name + '.passwd'],
                'db': self.property[name + '.db'],
                'port': int(self.property[name + '.port']),
                'charset': charset,
                'connect_timeout': 30
            }
            if name != 'test':
                # 写数据使用DRDS
                write_conf = {
                    'host': self.property['drds.host'],
                    'user': self.property['drds.user'],
                    'passwd': self.property['drds.passwd'],
                    'db': self.property['drds.db'],
                    'port': int(self.property['drds.port']),
                    'charset': charset,
                    'connect_timeout': 30
                }
                self.dbs[name] = DBUtil(read_conf, write_conf)
            else:
                self.dbs[name] = DBUtil(read_conf, read_conf)
        return self.dbs[name]


factory = DBFactory()

if __name__ == '__main__':
    db = factory.get_db('pay')
    print db.__dict__
    print db.fetch_data_with_map('select * from b_user limit 1')
