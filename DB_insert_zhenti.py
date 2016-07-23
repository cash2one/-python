#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
#conn = MySQLdb.connect(host="",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8")
conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "root", db = "cidian_iciba", charset = "utf8")

def process():
    cursor = conn.cursor()
    for line in open('/Users/bjhl/Documents/cidian/cidian_haici.log'):
        _dict = json.loads(line.replace('\\\\','\\'))
        word = _dict['word'].strip()
        #print type
        paraphrase = json.dumps(_dict['paraphrase'])
        example = json.dumps(_dict['example'])
        annotation = json.dumps(_dict['annotation'])
        related_word = json.dumps(_dict['related_word'])

        print '%s' % word
        try:
            sql = """
                update tb_cidian set paraphrase=%s, example=%s, annotation=%s, related_word=%s  where word = %s
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(paraphrase, example, annotation, related_word, word))
            conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()