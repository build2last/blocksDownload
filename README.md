# python 分块多线程下载器
将通过 HTTP 协议传输的文件进行分块，并用多线程下载，充分利用本地带宽。

### 说明
* 只需要 python 2.7 , 不需要三方库。
* 每个线程对应一个 http 连接
* max_block_size 越大内存占用越大，影响数据能否尽早写入磁盘而不是停留在内存里。单个下载块太大会出 **MemoryError**
* 经过测试：压缩文件，视频文件，音频文件没问题，但有些网站的安装包无法打开，什么"缺少端对端验证"
* 目前网上大多电影都是通过 p2p 方式分享的，所以这个程序可能并没有太大的作用
* 优先根据指定的 threading 数量设定线程数目，不指定的话将会根据 max_block_size 大小计算合适的线程个数。
* 利用 Event 事件实现进程同步。
* 请谨慎使用test，因为会在下载会破坏性覆盖同名文件。
> 下载[阴阳师apk](http://g37.gdl.netease.com/onmyoji_netease_9_1.0.17.apk)提速效果还是很明显的。

### downloader:
    def __init__(self, url, download_to, max_block_size=1024*1024*5, thread_num=0):
    * url:待下载文件链接
    * download_to：存放下载文件的路径
    * max_block_size：可能出现的最大的下载块大小, 单位 Byte
    * thread_num: 制定下载线程个数，缺省会根据 max_block_size 自动计算
    > thread_num 的自定义会导致根据 max_block_size 计算失效

### 适用于：
* 通过 http 协议传输的大型文件(>200MB)
* 服务器端未对单个主机的链接个数进行限制或者限制已知。

### Update Note:
1. 2017-04-07
		实现了分块多线程下载的功能，但要构建一个健壮的下载器，还有很多细节需要考虑，需要更多包装。
		比如：(1)提供 FTP 协议的兼容，(2)更人性化的使用方法包装