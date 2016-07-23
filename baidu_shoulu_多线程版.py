#coding:utf-8
import pycurl,re,StringIO
import  threading,Queue,time

class caiji:
        #打开网页  url：网页URL
        def html(self,url):
                while 1:
                        try:
                                b=StringIO.StringIO()
                                c=pycurl.Curl()
                                c.setopt(pycurl.URL,url) #打开URL
                                c.setopt(pycurl.FOLLOWLOCATION,2) #允许跟踪来源，有参数：1和2
                                c.setopt(pycurl.ENCODING, 'gzip')  #开启gzip压缩提高下载速度
                                c.setopt(pycurl.NOSIGNAL, True)   #开启后多线程不会报错
                                c.setopt(pycurl.MAXREDIRS,1) #最大重定向次数，0表示不重定向
                                c.setopt(pycurl.CONNECTTIMEOUT,60) #链接超时
                                c.setopt(pycurl.TIMEOUT,30)  #下载超时
                                c.setopt(pycurl.USERAGENT,'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)')
                                #pycurl.USERAGENT  模拟浏览器
                                c.setopt(pycurl.WRITEFUNCTION, b.write)  #回调写入字符串缓存
                                c.perform() #执行上述访问网址的操作
                                # print c.getinfo(pycurl.HTTP_CODE)
                                c.close()
                                html=b.getvalue()   #读取b中的数据
                                return html    #跳出并返回html
                        except:
                                continue


wurl=open(r"url收录结果.txt",'a')

caiji=caiji()

class count:
        def __init__(self):
                self.shoulu=0
                self.wshoulu=0
                self.i=0
                self.lock=threading.Lock()


        def c_wshoulu(self):
                self.lock.acquire()
                self.wshoulu+=1
                wshoulu=self.wshoulu
                self.lock.release()
                return wshoulu


        def c_sl(self):
                self.lock.acquire()
                self.shoulu+=1
                shoulu=self.shoulu
                self.lock.release()
                return shoulu


        def c_i(self):
                self.lock.acquire()
                self.i+=1
                i=self.i
                self.lock.release()
                return i

count=count()

class th(threading.Thread):
        def __init__(self,qurl):
                threading.Thread.__init__(self)
                self.qurl=qurl
                self.lock=threading.Lock()
                self.cond=threading.Condition()


        def run(self):
                while 1:
                        ddc=self.qurl.get()
                        if ddc is  None:
                                break
                        while 1:
                                bdhtm=caiji.html('http://www.baidu.com/s?wd='+ddc)
                                self.lock.acquire()

                                if '抱歉，没有找到与' in bdhtm:
                                    i = count.c_i()
                                    print '第%s条, %s ,未收录' % (i, ddc)
                                    wurl.writelines('第%s条, %s ,未收录\n' % (i, ddc))
                                    count.c_wshoulu()
                                    break
                                elif '百度为您找到相关结果约' in bdhtm:
                                        i=count.c_i()
                                        print '第%s条, %s ,收录'% (i,ddc)
                                        wurl.writelines('第%s条, %s ,收录\n'% (i,ddc))
                                        count.c_sl()
                                        break


                                elif 'http://verify.baidu.com/' in bdhtm:
                                        print ddc,'出现验证码，等待5分钟后自动开始'
                                        self.lock.release()
                                        time.sleep(500)
                                        continue

                                else:
                                        print 'Error'
                                        break
                        self.lock.release()


qurl=Queue.Queue(0)
threadCount=6    #开启线程数，默认6个线程

ths=[]
for t in range(threadCount):
        thread=th(qurl)
        thread.start()
        ths.append(thread)

for ddc in open(r'url.txt'):   #导入需要查询的URL文件，格式必须是utf-8
        ddc=ddc[0:-1]
        qurl.put(ddc)

for tt in range(threadCount):
        qurl.put(None)

for t in ths:
        t.join()

sl=count.c_sl()-1

print  '\n收录率：'+str(round(float(sl)/float(count.c_i()-1)*100,2)),"%"
print '收录：%s 条'%str(sl)
print '未收录：%s 条'%str(count.c_wshoulu()-1)