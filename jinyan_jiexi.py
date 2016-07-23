#ecoding:utf-8
import json
import traceback
import sys
import datetime
import urllib2, urllib
import urlparse
from pyquery import PyQuery
from lxml import etree
import time
import requests

import os
#os.putenv('http_proxy', '119.188.94.145:80')
#proxies = {'http': '119.188.94.145:80'}

reload(sys)
sys.setdefaultencoding("utf-8")
fw_error = open('/Users/bjhl/Documents/error.log','a')
def get_article_url():
    deal_list = [
        #['高考', 'gaokao.log', 2181],
        ['留学', 'liuxue.log', 1261],
        ['考研', 'kaoyan.log', 1061],
        ['公务员', 'gongwuyuan.log', 1031],
        ['中考', 'zhognkao.log', 471]
    ]
    fw = open('gaokao_urls.log', 'a')

    for i in range(2000, 2180, 10):
        print i
        url = 'http://jingyan.baidu.com/tag?tagName=%E9%AB%98%E8%80%83&rn=10&pn=' + str(i)
        try:
            html = urllib2.urlopen(url).read()
            tree = etree.HTML(html)
            for node in tree.xpath("//a/@href"):
                if 'article' in node:
                    fw.write(node + '\n')
                    fw.flush()
        except:
            traceback.print_exc()
        time.sleep(5)
    fw.close()

def get_content(url, filename, type=1):
    try:
        if type == 1:
            #print url
            #content = urllib2.urlopen(url).read()
            #content = requests.get(url).read()
            content = urllib2.urlopen(url, timeout=5).read()
            #print content
        else:
            content = ''
            #with open('/Users/bjhl/Downloads/20b68a8852ef1f796dec6273.html') as f:
            #with open('/Users/bjhl/Downloads/86fae346b45e653c48121a48.html') as f:
            #with open('/Users/bjhl/Downloads/f79b7cb3bb97629145023e50.html') as f:
            with open(url) as f:
                for line in f:
                    content += line.strip('\n')
    except:
        traceback.print_exc()
        fw_error.write(filename+'\x01'+url+'\n')
        fw_error.flush()
        return None

    return content

def parse_detail(url, filename):
    if 'genshuixue' not in url:
        #url = 'http://jingyan.baidu.com' + url
        pass
    #html = urllib2.urlopen(url).read()
    content = get_content(url, filename)
    if not content:
        return
    jq = PyQuery(content)
    res_json = {
        'bread': jq('.bread-wrap').text().replace('>','').split()[-2:],
        'title': jq('h1').text().replace('听语音',''),
        'date':  jq('time').text()[:10],
        'source': 'baidu',
        'url': url.replace('\n',''),
        'class': 36,
        'subject': u'经验',
        'data_weight': 0,
    }
    methods = []
    content = [each for each in jq('.exp-content-block')]
    print len(content)
    if not content:
        return None
    elif len(content) == 1:
        _list = []
        for steps in PyQuery(content[0])('ol li'):
            step = PyQuery(steps)
            step_title = step.text()
            image = step.html()
            img = image.split('data-src="')[-1].split('"')[0] if image and '<img' in image else ''
            #print img
            _list.append({
                'img': img,
                'title': step_title,
                'substeps': [],
            })
        methods.append(_list)
        abstract = {}
    else:
        try:
            question_desc_img = PyQuery(content[0])('.content-listblock-image').html().split('data-src="')[-1].split('"')[0]
        except:
            question_desc_img = ''
        abstract = {
            'title': '',
            'steps': [PyQuery(content[0])('p').text(),],
            'img': question_desc_img
        }
        for each in content[1:]:
            method = PyQuery(each)
            title = method('h2').text()
            #print title
            _list = []
            steps_list = [step for step in method('ol li')]
            if not steps_list:
                steps_list = [step for step in method('ul li')]
            for steps in steps_list:
                step = PyQuery(steps)
                step_title = step.text()
                image = step('.content-list-image a').html()
                img = image.split('data-src="')[-1].split('"')[0] if image else ''
                _list.append({
                    'img': img,
                    'title': step_title,
                    'substeps': [],
                })
            if not _list:
                _list.append((method('.content-listblock-text').text()))
            methods.append({'title': title, 'steps': _list})
        #工具
        if methods[0]['title'] == u'工具/原料':
            prepare = {'title': methods[0]['title'], 'steps': [v['title'] for v in methods[0]['steps']]}
            methods = methods[1:]
            res_json['prepare'] = prepare
        #注意事项
        if len(methods) == 0:
            return None

        if methods[-1]['title'] == u'注意事项':
            summary = {'title': methods[-1]['title'], 'steps': [v['title'] for v in methods[-1]['steps']]}
            methods = methods[:-1]
            res_json['summary'] = summary
    res_json['methods'] = methods
    res_json['abstract'] = abstract
    #print json.dumps(res_json)
    return json.dumps(res_json)

def get_files():
    file_list = os.listdir('./jingyan/')
    with open('dst_url') as f:
        for line in f:
            url = line.strip('\n')
            file = url.split('/')[-1]
            #print os.system('wget %s .'%line.strip('\n'))
            if file in file_list:
                continue
            print os.system('wget -T 5 %s .'%line.strip('\n'))
            time.sleep(1)

if __name__ == '__main__':
    #get_article_url()
    i = 0
    folder = '/Users/bjhl/Documents/baidujinyan_result'
    json_folder = '/Users/bjhl/Documents/baidujinyan_json'
    for file in os.listdir(folder):
        if '.log' not in file:
            continue
        src_file = '%s/%s' % (folder,file)

        with open(src_file) as f:
            fw = open(json_folder+'/'+file,'a')
            for line in f:
                #url = 'http://jingyan.baidu.com' + line
                url = line
                print url
                #if i == 0:
                    #i += 1
                json_file = parse_detail(url,str(file))
                if json_file == None:
                    continue
                fw.write(json_file+'\n')
                fw.flush()
                #time.sleep(2)
                #break
            fw.close()
            print str(file)+'已爬完'+'\n'
            #break
    fw_error.close()
        #break
    # get_files()
