#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2,re,platform
from datetime import *

#urlib2抓取网页
def getContent(url, timeout=5):
	content = None
	try:
		res = urllib2.urlopen(url, timeout=timeout)
		content = res.read()
	except urllib2.URLError, e:
		print e.reason
	return content

#正则匹配IP地址和域名
def getMain(content):
	content = content.replace('&nbsp;',' ')
	r = re.compile(r'<\s*br\s*/\s*>')
	content = r.sub("\n", content)
	r = re.compile(r'([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])\.([1]?\d\d?|2[0-4]\d|25[0-5])\s+([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}')
	r2 = re.compile(r'\s+')
	ms = []
	for m in r.finditer(content):
		ms.append(r2.sub("\t",m.group()).strip())
	return "\n".join(ms)



#source host url
url = 'http://www.360kb.com/kb/2_122.html'

#标示字符串
keychars = '#google hosts'


if __name__ == '__main__':
	#获取当前操作系统，判断修改文件路径
	syst = platform.system()
	if syst=='Windows':
		#windows
		hosts = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
	else:
		#linux
		hosts = '/etc/hosts'
	print 'get_page_content:'
	content = getContent(url, 5)
	if content==None:
		print 'page_content_none'
		exit
	print 'get_host_content:'
	hostcontents = getMain(content)
	uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	hostcontents = keychars+' '+uptime+"\n"+hostcontents+"\n"+keychars+' end'
	print 'open_host_file'
	fp = open(hosts, 'rb')
	c = fp.read()
	fp.close()

	pos1 = c.find(keychars)
	if pos1==-1:
		result = c+"\n"*2+hostcontents
	else :
		result = c[:pos1]+"\n"*2+hostcontents
	print 'write_hosts'
	fp = open(hosts, 'wb')
	fp.write(result)
	fp.close()

	print 'complete!'