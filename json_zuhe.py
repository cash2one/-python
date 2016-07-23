#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(host = "127.0.0.1", user = "zhanqun", passwd = "wdlPD40xjO5", db = "zhanqun", charset = "utf8", port = 3305)

def process():
    cursor = conn.cursor()
    res_json = {}
    try:
        sql = """
            select * from tb_cidian where id = 317
        """
        #print (url, word, type, pronunciation, character, other_meaning, change, level)
        cursor.execute(sql)
        for (id, url, word, ci_type, pronunciation, ci_character, other_meaning, ci_change, ci_level, paraphrase, example, annotation, question, dict, related_word) in cursor.fetchall():
            res_json['id'] = id
            res_json['word'] = word
            res_json['ci_type'] = ci_type
            res_json['pronunciation'] = json.loads(pronunciation)
            res_json['ci_character'] = json.loads(ci_character)
            res_json['other_meaning'] = json.loads(other_meaning)
            res_json['ci_change'] = ci_change
            res_json['ci_level'] = ci_level
            res_json['paraphrase'] = json.loads(paraphrase)
            res_json['example'] = json.loads(example)
            res_json['annotation'] = json.loads(annotation)
            res_json['question'] = json.loads(question)
            res_json['dict'] = json.loads(dict)
            res_json['related_word'] = json.loads(related_word)
        print json.dumps(res_json)
    except:
        traceback.print_exc()
if __name__ == '__main__':
    process()