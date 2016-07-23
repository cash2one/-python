#encoding=utf-8
#批量查询百度收录。统计收录率、收录数据共多少条，未收录数据共多少条
#http://www.seoqx.com/论坛账号:0422
import urllib,time
import StringIO
import pycurl

def get_baidu_html(url):
    html = StringIO.StringIO()
    c = pycurl.Curl()
    myurl="http://www.baidu.com/s?wd=%s"%url
    c.setopt(pycurl.URL, myurl)
    #写的回调
    c.setopt(pycurl.WRITEFUNCTION, html.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    #最大重定向次数,可以预防重定向陷阱
    c.setopt(pycurl.MAXREDIRS, 5)
    #连接超时设置
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.TIMEOUT, 300)
    #模拟浏览器
    c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
    #访问,阻塞到访问结束
    ret = c.perform()
    #输出网页的内容
    ret = html.getvalue()
    if '<div class="nors"><p>很抱歉，没有找到与' in ret or 'class=f14>没有找到该URL。您可以直接访问' in ret:
        print url,'未收录'
        return
    elif "百度为您找到相关结果" in ret:
        print url, '成功被收录'
        return 1
    elif "http://verify.baidu.com" in ret:
        print "查询过程出现验证码"
        time.sleep(300)
        return


if __name__=="__main__":
    urls=open('url.txt','r').readlines()
    oknum=0
    lostnum=0
    for url in urls:
        #print url.strip()   #ctrl+/
        if get_baidu_html(url.strip()):
            oknum+=1
        else:
            lostnum+=1

    print '收录率：',float(oknum)/(oknum+lostnum)*100,'%'
    print "收录数据共 %s 条"%oknum
    print "未收录数据共 %s 条"% lostnum

