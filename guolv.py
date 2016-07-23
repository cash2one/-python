#ecoding:utf-8
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
folder = '/Users/bjhl/Documents/baidujinyan_json'
guolv_folder = '/Users/bjhl/Documents/baidujingyan_guolv'
for file in os.listdir(folder):
    if '.log' not in file:
        continue
    src_file = '%s/%s' % (folder, file)
    with open(src_file) as f:
        fw = open(guolv_folder + '/' + file, 'a')
        for line in f:
            if '[[]]' in line:
                continue
            line = line.replace('[[{','[{"steps": [{').replace('}]], "source":','}], "title": "\u65b9\u6cd5/\u6b65\u9aa4"}], "source":')

            fw.write(line)
            fw.flush()
        fw.close()