# coding:utf-8

#-----Python 3 Compatible
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#---------------------------------
import urllib
import urllib2
import threading
import time
import datetime

class downloader:
    def __init__(self, url, download_to, max_block_size=1024*1024*5, thread_num=0):
        self.url = url
        self.name = download_to
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req)
        file_size = response.headers.getheader('Content-Length')
        self.total = int(file_size)
        # 根据要求或者块大小计算线程个数
        if thread_num:
        	self.thread_num = thread_num
        else:
        	self.thread_num = (self.total+max_block_size-1)//max_block_size
        print(self.thread_num)
        self.event_list = [threading.Event() for _ in range(self.thread_num)]
        self.event_list[0].set()
        print('File size is %d KB'%(self.total/1024))

    # 划分每个下载块的范围
    def get_range(self):
        ranges=[]
        offset = int(self.total/self.thread_num)
        for i in range(self.thread_num):
            if i == self.thread_num-1:
                ranges.append((i*offset,''))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges

    def download(self,start,end, event_num):
        post_data = {'Range':'Bytes=%s-%s' % (start,end),'Accept-Encoding':'*'}
        # headers = urllib.urlencode(post_data)
        req = urllib2.Request(self.url, headers=post_data)
        res = urllib2.urlopen(req)
        # res = requests.get(self.url,headers=headers)
        print('%s:%s chunk starts to download'%(start,end))
        self.event_list[event_num].wait()
        self.fd.seek(start)
        self.fd.write(res.read())
        print("Number[%d] block was written"%event_num)
        if event_num<len(self.event_list)-1:
            self.event_list[event_num+1].set()

    def run(self):
        self.fd =  open(self.name,'ab')
        thread_list = []
        n = 0
        for ran in self.get_range():
            start,end = ran
            print('thread %d Range:%s ~ %s Bytes'%(n, start, end))
            thread = threading.Thread(target=self.download, args=(start,end,n))
            thread.start()
            thread_list.append(thread)
            n += 1
        map(lambda thd:thd.join(), thread_list)
        print('download %s load success'%(self.name))
        self.fd.close()
