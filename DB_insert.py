#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "root", db = "cidian_iciba", charset = "utf8")

def process():
    cursor = conn.cursor()
    for line in open('/Users/bjhl/Documents/cidian/cidian_iciba.log'):
        _dict = json.loads(line.replace('\\\\','\\'))
        url = _dict['url']
        title = _dict['title']
        word = _dict['word'].strip()
        type = _dict['type']
        #print type
        pronunciation = json.dumps(_dict['pronunciation'])
        character = json.dumps(_dict['character'])
        other_meaning = json.dumps(_dict['other_meaning'])
        change = _dict['change']
        level = _dict['level']

        print '%s' % word
        try:
            sql = """
                insert into tb_cidian (url, word, ci_type, pronunciation, ci_character, other_meaning, ci_change, ci_level) values(%s, %s, %s, %s, %s, %s, %s, %s)
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(url, word, type, pronunciation, character, other_meaning, change, level))
            conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()