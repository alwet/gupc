# coding=utf-8
from time import sleep, ctime 
import re
import chardet
import sys
import urllib
import urllib2
import threading
import multiprocessing
import sys
import random
import math

def getHtml(url):
	try:
		page = urllib2.urlopen(url,timeout=60+30)
	except urllib2.HTTPError, e:
		print "sstal:%s"%url
		#raise e
		return '0'
	except :                                    #其它异常
		print "debug" 
		return '0'
	#sleep(random.randrange(100,400)/100.0+3)
	html = page.read()
	print url
	return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist      
def print_file(txt,file_w):
	output = open(file_w, 'w')
	output.write(txt)
	output.close()

def get_value(id):
	#mm=re.search(r'6\d{5}',id)
	if(re.match(r'6\d{5}',id)):
		tem="sh"+id;
	else:
		tem="sz"+id;
	url="http://f9.eastmoney.com/%s.html"%tem
	#print url
	#url="http://f9.eastmoney.com/sh600001.html"
	#url=r"http://tieba.baidu.com/p/2460150866"
	html = getHtml(url)#akdkf
	#print 'Html is encoding by : %',chardet.detect(getHtml(url))
	#a = html.decode('GB2312').encode('utf-8');
	a = html.decode('GBK').encode('utf-8');
	reg=r'稀释每股收益\(元\)<\/td><td>([\d\.\-]+)<\/td><td>.*净利润滚动环比增长\(%\)<\/td><td>([\d\.\-]+)<\/td><td>'
	mm = re.search(reg,a) 
	if mm :
		if re.match(r'--',mm.groups()[0]):
			print "稀释每股收益是--"
			return '0'
		xiuimzguubyi=float(mm.groups()[0])
		if xiuimzguubyi<=0:
			print "稀释每股收益小于等于0"
			return '0'
		if re.match(r'--',mm.groups()[1]):
			print "净利润滚动环比增长是--"
			return '0'
		lirvtsbi=float(mm.groups()[1])
		if lirvtsbi<=0:
			print "利润同比增加率小于等于0"
			return '0'
	else:
		return '0'
	reg=r'(\S+?)\(%s\)深度F9 V1.0 '%id
	mm=re.search(reg,a)
	if mm:
		name=mm.groups()[0]
	else:
		return '0'
	url="https://gupiao.baidu.com/stock/%s.html"%tem
	html = getHtml(url)#akdkf
	reg=r'''div class=\"price s-(\w+) \">\n                        <strong  class=\"_close\">([\d\.]+)<\/strong>'''
	mm=re.search(reg,html,re.S|re.M)
	if mm :
		ud=mm.groups()[0]
		price=float(mm.groups()[1])
	else :
		return '0'
	#print mm.group()
	#print (type(a))
	#print sys.getfilesystemencoding()  
	#print 'Html is encoding by : %',chardet.detect(getHtml(url))
	#print_file(html,'b')
	#print_file(a,'ba')
	#print getImg(html)
	if (xiuimzguubyi==0 or lirvtsbi==0):
		return '0'
	#return [id,name,'%.6f'%(price/xiuimzguubyi/lirvtsbi),str(price),str(ud),str(xiuimzguubyi),str(lirvtsbi)];
	return [id,name,'%.6f'%(price/xiuimzguubyi/math.sqrt(lirvtsbi)),str(price),str(ud),str(xiuimzguubyi),str(lirvtsbi)];
def store_value(self,begin,end,f_name):
	print begin,end,f_name;
	f_name_str='../../../perl_code/gupc/gupc_data/'+"%06d"%(f_name)+'.csv'
	#f_name_str='./'+"%06d"%(f_name)+'.csv'
	file_object = open(f_name_str, 'w')
	#for i in range(begin,end):
	i=begin
	while i <= end:
		#print i;
		i_str="%06d"%(i)
		tem=get_value(str(i_str))
		#tem=(begin,end,f_name)
		temc=','.join(tem)
		file_object.write(temc+'\n');
		i=i+1;
	file_object.close( )
def test(a,b,c):
	print "begin"
	sleep(10)
	print "end"
	return 0
	
def muti_thread(bg_code,max_threads):
	jmge=10;
	#max_threads=340;
	#bg_code=600000
	threads = []
	for ciuu in range(max_threads):
		t = threading.Thread(target=store_value,args=(store_value,bg_code+ciuu*jmge,bg_code+(ciuu+1)*jmge-1,ciuu+bg_code))
		#sleep(2)
		threads.append(t)
	for ciuu in range(max_threads):
		threads[ciuu].start() 
		sleep(random.randrange(0,200)/100.0)
	for ciuu in range(max_threads):
		print "waitting %d thread"%ciuu
		threads[ciuu].join()
	print "all thread is over "
		
def muti_process(bg_code,max_threads):
	jmge=10;
	for ciuu in range(max_threads):
		p = multiprocessing.Process(target=store_value,args=(bg_code+ciuu*jmge,bg_code+(ciuu+1)*jmge-1,ciuu+bg_code))
		p.daemon = True
		p.start()
		p.join()
	print "all thread is over "
		

if __name__ == "__main__" :
	#a=store_value(3,600000,600100,600000)
	muti_thread(int(sys.argv[1]),int(sys.argv[2]))
	#muti_process(int(sys.argv[1]),int(sys.argv[2]))
	#print a
