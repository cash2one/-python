#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict

__author__ = 'Will Wang <wangweiwei@baijiahulian.com>'
__version__ = "1.2.0"
__date__ = "15/1/9"
__doc__ = """
            1.增加fetch_by_map方法
            2.增加使用params取数据方法
            3.增加将dict数据直接插入到mysql的方法
            4.增加读写使用不同的数据库连接
            """

import MySQLdb


class DBUtil():
    def __init__(self, reader, writer):
        if not isinstance(reader, dict):
            raise TypeError
        self.reader = reader
        if not writer:
            self.writer = reader
        else:
            self.writer = writer
        self.conn = None
        # 数据库写连接，使用drds
        self.conn_w = MySQLdb.connect(**self.writer)
        self.conn = MySQLdb.connect(**self.reader)

    def fetch_one(self, sql, params=None, auto_close=True):
        cur = None
        try:
            sql = sql.strip()
            cur = self.conn.cursor()
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            result = cur.fetchone()
            return result
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def fetch_all(self, sql, params=None, auto_close=True):
        """
        返回每行为Tuple
        :param sql:
        :param params:
        :return:
        """
        cur = None
        try:
            sql = sql.strip()
            cur = self.conn.cursor()
            cur.execute(sql, params)
            result = cur.fetchall()
            return result
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def fetch_data_with_map(self, sql, params=None, auto_close=True, columns=False):
        """
        返回数据为每行数据为一个map
        :param sql:
        :param params:
        :return:
        """
        cur = None
        try:
            sql = sql.strip()
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql, params)
            result = cur.fetchall()
            if columns:
                return result, self.get_columns(cur)
            else:
                return result
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def fetch_one_with_map(self, sql, params=None, auto_close=True):

        """
        返回数据为每行数据为一个map
        :param sql:
        :param params:
        :return:
        """
        cur = None
        try:
            sql = sql.strip()
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql, params)
            result = cur.fetchone()
            return result
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def stat(self, sql, params=None, auto_close=True):
        """
        Insert Delete Update等操作
        :param sql:
        :param params:
        :param auto_close:
        :return: 受影响的行数
        """
        cur = None
        try:
            cur = self.conn_w.cursor()
            infect_rows = cur.execute(sql, params)
            self.conn_w.commit()
            return infect_rows
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def insert(self, sql, params=None, auto_close=True):
        """
        Insert Delete Update等操作
        :param sql:
        :param params:
        :param auto_close:
        :return: 插入后的主键id
        """
        cur = None
        try:
            cur = self.conn_w.cursor()
            cur.execute(sql, params)
            insert_id = cur.lastrowid
            self.conn_w.commit()
            return insert_id
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def fetch_by_map(self, sql, key_column, value_column=None, params=None, auto_close=True):
        """
        :param sql:
        :param key_column:
        :param value_column:
        :param params:
        :param auto_close:
        :return: {key_column1:value_column1,key_column2:value_column2,...}
        """
        cur = None
        try:
            sql = sql.strip()
            result_map = {}
            # 获取字典cursor,默认cursor取回的是tuple数据
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql, params)
            result = cur.fetchall()
            if value_column:
                for row in result:
                    result_map[row[key_column]] = row[value_column]
            else:
                for row in result:
                    result_map[row[key_column]] = row
            return result_map
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def fetch_by_map_list(self, sql, key_column, value_column=None, params=None, auto_close=True, columns=False):
        """
        解决key重复的问题，如果相同的key则默认在list上追加
        :param sql:
        :param key_column:
        :param value_column:
        :param params:
        :return:
        """
        cur = None
        try:
            sql = sql.strip()
            result_map = defaultdict(list)
            # 获取字典cursor,默认cursor取回的是tuple数据
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql, params)
            result = cur.fetchall()
            if value_column:
                for row in result:
                    result_map[row[key_column]].append(row[value_column])
            else:
                for row in result:
                    result_map[row[key_column]].append(row)
            if columns:
                return result_map, self.get_columns(cur)
            else:
                return result_map
        except Exception, e:
            if params:
                print sql % params
            else:
                print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def insert_dict_data(self, table, data_dict, auto_close=True):
        """
        将一个dict对象按照key=column_name, value=column_value插入到数据库中
        :param table:
        :param data_dict:
        :param auto_close:
        :return:
        """
        qmarks = ', '.join(['%s'] * len(data_dict))
        cols = ', '.join(data_dict.keys())
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
        cur = None
        try:
            cur = self.conn_w.cursor()
            cur.execute(sql, data_dict.values())
            self.conn_w.commit()
        except Exception, e:
            print sql
            raise e
        finally:
            if cur and auto_close:
                cur.close()

    def get_columns(self, cur):
        """
        获取游标字段
        :param cur:
        :return:
        """
        return [c[0] for c in cur.description]

    def close_cursor(self):
        if self.conn and self.conn.cursor:
            self.conn.cursor.close()


if __name__ == '__main__':
    db = DBUtil()
    _map = db.fetch_by_map("select * from b_role", "id")
    print _map
