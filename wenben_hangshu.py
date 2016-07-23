#ecoding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
result_folder = '/Users/bjhl/Documents/baidujingyan_guolv'
count = 0
for file in os.listdir(result_folder):
    src_file = '%s/%s' % (result_folder,file)
    with open(src_file) as f:
        count += len(f.readlines())
        print count
print '总行数' + str(count)


