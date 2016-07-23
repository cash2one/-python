#ecoding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
folder = '/Users/bjhl/Documents/baidujinyan'
result_folder = '/Users/bjhl/Documents/baidujinyan_result'
for file in os.listdir(folder):
    src_file = '%s/%s' % (folder,file)
    with open(src_file) as f:
        urls = f.readlines()
        only_urls = set(urls)
        fw = open(result_folder + '/' + file, 'a')
        for url in only_urls:
            fw.write(url)
            fw.flush()
        fw.close()


