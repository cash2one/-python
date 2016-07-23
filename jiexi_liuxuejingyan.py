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
        'bread': [u'美国留学'],
        'title': title,
        'date': date,
        'source': u'天道',
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
    try:
        question_desc_img = PyQuery(content[1]).html().split('src="')[1].split('"')[0]
    except:
        question_desc_img = ''
    flag_abstract = True
    flag_method = False
    flag_first = True
    steps = ['']
    _list = []
    img = ''
    step_title = ''
    substeps = []
    index = 2
    if question_desc_img == '':
        index = 1
    for each_json in content[index:]:
        each = (PyQuery(each_json).remove('a').html())
        #print each
        #print each[1].decode('utf8')
        #break
        if each == 'None' or each.strip() == '':
            continue
        if u'相关阅读' in each or u'扫一扫' in each or u'相关链接' in each or u'天道提示' in each:
            break
        #print each
        if 'strong' in each or u'【' in each or each.strip()[1] == u'、' or each.strip()[1] == u'.' \
                or u'常识之' in each or (u'常识' in each and u'、' in each) or (len(each.strip()) < 10 and u'：' not in each) or each.strip()[-1] == u'：':
            flag_abstract = False
        if flag_abstract:
            steps.append(PyQuery(each_json).remove('a').text())
        else:
            if 'strong' in each or u'【' in each or each.strip()[1] == u'、' or each.strip()[1] == u'.' \
                    or u'常识之' in each or (u'常识' in each and u'、' in each) or (len(each.strip()) < 10 and u'：' not in each) or each.strip()[-1] == u'：':
                #print each.strip()[1]
                if not flag_first:
                    _list.append({
                        'img': img,
                        'title': step_title,
                        'substeps': substeps,
                    })
                    img = ''
                    step_title = '<strong>'+PyQuery(each_json).remove('a').text()+'</strong>'
                    substeps = []
                if flag_first:
                    step_title = '<strong>'+PyQuery(each_json).remove('a').text()+'</strong>'
                    flag_first = False
            elif 'text-align: center;' in each and 'src="' in each:
                img = each.split('src="')[1].split('"')[0]
            else:
                substeps.append(PyQuery(each_json).remove('a').text())
    _list.append({
        'img': img,
        'title': step_title,
        'substeps': substeps,
    })
    methods.append({'title': u'方法/步骤', 'steps': _list})
    steps[0] = PyQuery(content[0]).text()
    abstract = {
        'title': '',
        'steps': steps,
        'img': question_desc_img,
    }
    res_json['methods'] = methods
    res_json['abstract'] = abstract
    #print res_json
    #print methods
    #print json.dumps(res_json)
    good =True
    if len(methods) == 0:
        good =False
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
                print url
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
                # if i == 1:
                #     break
            fw.close()
            #break