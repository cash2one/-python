#ecoding:utf-8
import  sys
import os, time
reload(sys)
sys.setdefaultencoding("utf-8")
while 1:
    os.system("kill -9 `ps -ef | grep Google | awk '{print $2}'`")
    time.sleep(60)