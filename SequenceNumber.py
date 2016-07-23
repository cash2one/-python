#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import log

__author__ = 'Will Wang <wangweiwei@baijiahulian.com>'
__version__ = "1.0.0"
__date__ = "15/11/10"


class SequenceNumber(object):
    _SUFFIX_TEACHER = 8
    _SUFFIX_STUDENT = 6
    _SUFFIX_ORGANIZATION = 9
    _WIDTH_ACCOUNT = 8
    bitmap = {
        4: [10, 2, 11, 3, 0, 1, 9, 7, 12, 6, 4, 8, 5],
        5: [4, 3, 13, 15, 7, 8, 6, 2, 1, 10, 5, 12, 0, 11, 14, 9],
        6: [2, 7, 10, 9, 16, 3, 6, 8, 0, 4, 1, 12, 11, 13, 18, 5, 15, 17, 14],
        7: [18, 0, 2, 22, 8, 3, 1, 14, 17, 12, 4, 19, 11, 9, 13, 5, 6, 15, 10, 16, 20, 7, 21],
        8: [11, 8, 4, 0, 16, 14, 22, 7, 3, 5, 13, 18, 24, 25, 23, 10, 1, 12, 6, 21, 17, 2, 15, 9, 19, 20],
        9: [24, 23, 27, 3, 9, 16, 25, 13, 28, 12, 0, 4, 10, 18, 11, 2, 17, 1, 21, 26, 5, 15, 7, 20, 22, 14, 19, 6,
            8],
        10: [32, 3, 1, 28, 21, 18, 30, 7, 12, 22, 20, 13, 16, 15, 6, 17, 9, 25, 11, 8, 4, 27, 14, 31, 5, 23, 24, 29,
             0, 10, 19, 26, 2],
        11: [9, 13, 2, 29, 11, 32, 14, 33, 24, 8, 27, 4, 22, 20, 5, 0, 21, 25, 17, 28, 34, 6, 23, 26, 30, 3, 7, 19,
             16, 15, 12, 31, 1, 35, 10, 18],
        12: [31, 4, 16, 33, 35, 29, 17, 37, 12, 28, 32, 22, 7, 10, 14, 26, 0, 9, 8, 3, 20, 2, 13, 5, 36, 27, 23, 15,
             19, 34, 38, 11, 24, 25, 30, 21, 18, 6, 1]
    }

    def encode_user_number(self, user_id):
        """
        user_id编码user_number
        :param user_id:
        :return: user_number
        """
        return str(self.encode(user_id, 8)) + '8'

    def encode(self, uid, width):
        """
        id => number
        用户尾数为8，机构的尾数为9
        :param uid:
        :param width:
        :return:
        """
        maximum = int('9' * width)
        superscript = int(log(maximum) / log(2))
        r = 0
        sign = 0x1 << superscript
        uid |= sign
        mapbit = self.bitmap[width]
        for x in range(0, superscript):
            v = (uid >> x) & 0x1
            r |= (v << mapbit[x])
        r += maximum - pow(2, superscript) + 1
        return r

    def decode(self, number, width):
        """
        通用的number => id
        :param number:
        :param width:
        :return:
        """
        number /= 10
        maximum = int('9' * width)
        superscript = int(log(maximum) / log(2))
        number = number + pow(2, superscript) - maximum - 1
        r = 0
        mapbit = self.bitmap[width]
        for x in range(0, superscript):
            r |= ((number >> mapbit[x]) & 0x1) << x
        return r

    def decode_number(self, user_number):
        try:
            if not user_number or int(user_number) == 0:
                return ''
        except ValueError:
            return ''
        _number = str(user_number)
        if len(_number) == 9 and _number[-1] in ('8', '9'):
            return self.decode(int(user_number), 8)
        else:
            return user_number

sequence_number = SequenceNumber()

if __name__ == '__main__':
    sn = SequenceNumber()
    # uid = 1840367 number = 561179698
    # uid = 2135 number = 374154408
    print sn.encode(1840367, 8)
    print sn.decode_number(374154408)