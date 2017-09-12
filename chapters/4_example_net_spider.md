## [Python笔记](https://billy0920.github.io/python_tips)
### 想做就做——开发一个网络爬虫
要实现网络爬虫，其实只要做到3步：
1. 从“待抓取的url列表”中取一个url，获取对应的网页内容；
2. 解析页面中的url，如果存在未抓取的url，存入“待抓取的url列表”中;
3. 存储抓取的网页内容，以及保存已经访问过的url列表；
 源代码非常简单，如下：

```python
# -*- coding: cp936 -*-
#spider.py

#抓取网页内容，保存为文件
import urllib
import re

def getPage(url):
    data = ""
    try:
        info = urllib.urlopen(url);
        data = info.read();
    except:
        pass
    return data

oldurls = []
newurls = []
def parseUrl(baseURL, URL, data, oldurls, newurls):
    urlpattern = re.compile(r"href=\"([^\"]+)")
    urls = urlpattern.findall(data)
    for url in urls:
        if(not url.startswith("http://")):
            url = baseURL+url
        if not url in oldurls:
            newurls.append(url)

    return newurls

def test(baseurl, url):
    data = getPage(url)
    for URL in parseUrl(baseurl, url, data, [], []):
        open(URL.replace(":","_").replace("/","_"),"w").write(getPage(URL))

if __name__ == "__main__":
    test("http://www.secon.cn","http://www.secon.cn/wxcs/xgjq/jbmxg/")
```

首先，定义了一个函数getPage(url)，它接收一个url参数（形如 [http://xxx.xxx/xxx] 的字符串），调用urllib模块的open函数，读取该url对应网页的文本内容；

然后，定义一个parseUrl(baseURL, URL, data,oldurls, newurls)函数，该函数使用正则表达式找出所有的超链接（href="xxx"在网页中表示一个超链接），然后检查超链接是否以http开头，如果是，则是一个完全链接；如果不是，则用baseURL加上超链接的内容构造出完全链接。再检查该完全链接是否位于已经访问过的链接的列表中（用oldurls表示已经访问过的链接，避免多次访问同一个链接），如果未访问过，就保存到newurls中，否则就不处理（相当于丢弃掉）。

最后定义一个test(baseurl, url)函数，该函数先调用getPage(url)，得到一个页面，然后使用parseUrl解析该页面的内容，得到一份新的url列表，然后针对该列表中的url，再次执行getPage并保存相关的页面内容。由于url中的某些符号不能用作文件名，因此将这些符号替换成下划线，替换特殊符号之后的url作为文件名。

整个网络爬虫脚本虽然简单，但是基本的要素都已经具备了。再进一步，可以使用递归的方式，再获取新的页面之后，再将页面中的超链接解析出来保存到列表中，继续进行解析，如果执行，最终强制终止程序或者将所有相关的url都抓取结束，再也获取不到新的url为止。
 

网络爬虫是网络数据挖掘的基础，但是数据挖掘需要用到更多的技术，例如分词。
## [Python笔记](https://billy0920.github.io/python_tips)
