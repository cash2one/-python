#ecoding:utf-8
import json
import traceback
import sys
from pyquery import PyQuery
import os
reload(sys)
sys.setdefaultencoding("utf-8")
def parse_detail(title, date, url, content, filename):
    if not content:
        return None
    jq = PyQuery(content)
    res_json = {
        'bread': [u'公务员'],
        'title': title,
        'date': date,
        'source': u'zhonggong',
        'url': url,
        'class': 36,
        'subject': u'经验',
        'data_weight': 0,
    }
    methods =[]
    content = [each for each in jq('p').items() if each.text().strip() != '']
    print len(content)
    if not content:
        return None
    if len(content) == 0:
        return None
    flag_strong = False
    for each in content:
        if '<strong>' in PyQuery(each).html():
            flag_strong = True
            break
    flag_abstract = True
    flag_method = False
    flag_first = True
    steps = []
    _list = []
    img = ''
    step_title = ''
    substeps = []
    for each_json in content:
        each = (PyQuery(each_json).remove('a').text())
        if u'专题推荐' in each or u'官方微信' in each or u'点击查看' in each:
            break
        #print each
        #print each[1].decode('utf8')
        #break
        if each == 'None' or each.strip() == '':
            continue
        if u'注：' in each or u'相关阅读' in each or u'扫一扫' in each or u'相关链接' in each or u'天道提示' in each:
            break
        #print each
        if flag_strong:
            if '<strong>' in PyQuery(each_json).html():
                flag_abstract = False
                flag_method = True
            if flag_abstract:
                steps.append(each)
            else:
                if '<strong>' in PyQuery(each_json).html():
                    # print each.strip()[1]
                    if not flag_first:
                        # print step_title
                        _list.append({
                            'img': img,
                            'title': step_title,
                            'substeps': substeps,
                        })
                        img = ''
                        if u'：' in each and each.strip()[-1] != u'：':
                            step_title = '<strong>' + each.split(u'：')[0] + '</strong>'
                            substeps.append(each.split(u'：')[1])
                        else:
                            step_title = '<strong>' + each + '</strong>'
                            substeps = []
                    if flag_first:
                        # print step_title
                        if u'：' in each and each.strip()[-1] != u'：':
                            step_title = '<strong>' + each.split(u'：')[0] + '</strong>'
                            substeps.append(each.split(u'：')[1])
                        else:
                            step_title = '<strong>' + each + '</strong>'
                            substeps = []
                        flag_first = False
                else:
                    substeps.append(each)
        else:
            if each.strip()[1] == u'、' or each.strip()[1] == '.':
                flag_abstract = False
                flag_method = True
            if flag_abstract:
                steps.append(each)
            else:
                if each.strip()[1] == u'、' or each.strip()[1] == '.':
                    #print each.strip()[1]
                    if not flag_first:
                        #print step_title
                        _list.append({
                            'img': img,
                            'title': step_title,
                            'substeps': substeps,
                        })
                        img = ''
                        if  u'：' in each and each.strip()[-1] != u'：' :
                            step_title = '<strong>'+each.split(u'：')[0]+'</strong>'
                            substeps.append(each.split(u'：')[1])
                        else:
                            step_title = '<strong>' + each + '</strong>'
                            substeps = []
                    if flag_first:
                        #print step_title
                        if u'：' in each and each.strip()[-1] != u'：':
                            step_title = '<strong>' + each.split(u'：')[0] + '</strong>'
                            substeps.append(each.split(u'：')[1])
                        else:
                            step_title = '<strong>' + each + '</strong>'
                            substeps = []
                        flag_first = False
                else:
                    substeps.append(each)
    _list.append({
        'img': img,
        'title': step_title,
        'substeps': substeps,
    })
    if flag_method:
        methods.append({'title': u'方法/步骤', 'steps': _list})
        abstract = {
            'title': '',
            'steps': steps,
            'img': '',
        }
    else:
        _list1 = []
        for v in steps[1:]:
            _list1.append({
                'img': '',
                'title': v,
                'substeps': '',
            })
        methods.append({'title': u'方法/步骤', 'steps': _list1})
        if len(steps) == 0:
            steps = ['']
        abstract = {
            'title': '',
            'steps': [steps[0]],
            'img': '',
        }
    res_json['methods'] = methods
    res_json['abstract'] = abstract
    #print res_json
    #print methods
    good =True
    #print json.dumps(res_json)
    return json.dumps(res_json), good

if __name__ == '__main__':
    i = 0
    folder = '/Users/bjhl/Documents/liuxuejingyan'
    json_folder = '/Users/bjhl/Documents/liuxuejingyan_json'
    for file in os.listdir(folder):
        if '.log' not in file:
            continue
        src_file = '%s/%s' % (folder, file)

        with open(src_file) as f:
            fw = open(json_folder + '/' + file, 'a')
            fw2 = open(json_folder + '/good_' + file, 'a')
            i = 0
            for line in f:
                #print line.replace('\\\\','\\')
                _dict = json.loads(line.replace('\\\\','\\'))
                title = _dict['title']
                date = _dict['date']
                url = _dict['url']
                content = _dict['html']
                if u'每日一练' in title or u'专项练习' in title:
                    continue
                print '\n'+url
                #print content
                try:
                    json_file, good =parse_detail(title, date, url, content, str(file))
                except:
                    traceback.print_exc()
                    continue
                if json_file == None:
                   continue
                if not good:
                    fw.write(json_file + '\n')
                else:
                    fw2.write(json_file + '\n')
                fw.flush()
                fw2.flush()
                i += 1
                #if i == 20:
                 #  break
            fw.close()
            #break