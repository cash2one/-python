# _*_ coding: utf-8 _*_
import urllib

s = 'http://www.genshuixue.com/i-ielts/s/%E6%9C%BA%E7%BB%8F/'
ss = urllib.unquote(s).decode('utf-8', 'replace')
print urllib.unquote(s).decode('utf-8', 'replace')
print s,ss
we = 'http://www.genshuixue.com/i-ielts/a/1/4?p=3'
print we.split('?')[0]
print 'http://www.genshuixue.com/i-ielts/s/雅思自学/'.split('/')