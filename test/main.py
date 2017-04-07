# coding:utf-8
#-----Python 3 Compatible
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import threading
import datetime
from blocksDownload import downloader


def main():
    url = r"http://localhost/%CC%EC%B0%B2%C3%C5"
    import os
    import urllib
    file_name = urllib.unquote(url.split('/')[-1])
    if os.path.exists(file_name):
        os.remove(file_name)
    start = datetime.datetime.now()
    down = downloader(url, file_name, max_block_size=1024*1024*20)
    down.run()
    while threading.activeCount()>1:
        time.sleep(1)
    end = datetime.datetime.now()
    print("Time cost %d seconds"%(end-start).seconds)

if __name__ == '__main__':
    main()