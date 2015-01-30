#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
#@Author Space
#@Date 2015/1/30
#@Email g0dl0veu@163.com
#

import urllib2,re,platform

#urlib2抓取网页
def getContent(url, timeout=5):
	content = None
	try:
		res = urllib2.urlopen(url, timeout=timeout)
		content = res.read()
	except urllib2.URLError, e:
		print e.reason
	return content

#字符串查找关键词之前内容
def getMain(content, keychars='#google-hosts-2015'):
	pos1 = content.find(keychars)
	pos2 = content.find(keychars,pos1+len(keychars))
	m = content[pos1:pos2+len(keychars)]
	m = m.replace('&nbsp;',' ')
	r = re.compile(r'<[\w\s\/]+>')
	return r.sub("", m)

#source host url
url = 'http://www.360kb.com/kb/2_122.html'
#标示字符串
keychars = '#google-hosts-2015'

if __name__ == "__main__":
	#获取当前操作系统，判断修改文件路径
	syst = platform.system()
	if syst=='Windows':
		#windows
		hosts = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
	else:
		#linux
		hosts = '/etc/hosts'

	content = getContent(url, 5)
	if content==None:
		exit
	hostcontents = getMain(content,keychars)

	fp = open(hosts, 'rb')
	c = fp.read()
	fp.close()

	pos1 = c.find(keychars)
	if pos1==-1:
		result = c+"\n"*2+hostcontents
	else :
		result = c[:pos1]+"\n"*2+hostcontents

	fp = open(hosts, 'wb')
	fp.write(result)
	fp.close()
