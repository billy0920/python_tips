## [Python笔记](https://github.com/billy0920/python_tips/blob/master/content.md)
### Python学习总结——可爱的python

《可爱的python》从一个任务出发，给出一个具体的例子，并且不断的改进之，使读者逐渐领略到python的魅力。
然而，对于初学者来说，毕竟还是希望有一个ABC的方式来学习python。

那么好吧，我来写一篇ABC。

#### 1 python环境安装
##### 1.1 python解释器安装
从python的官网（请自行摆渡）下载最新的python安装程序，然后根据安装步骤进行安装即可。
推荐用2.7.x的版本。我不是故意跟python官方唱反调，python管方是推荐3.x版本的，但是从实践来看，2.x版本才是主流，而2.7.x版本则是非常稳定的主流版本，推荐！
python的msi安装程序安装完成之后，应该可以在新开的命令行窗口中输入python进入到python运行环境。如果命令行中无法直接运行python，则需要手工将python安装路径添加到Path环境变量中。

##### 1.2 python virtualenv安装
virtualenv是一个非常好用的python虚拟环境工具。为什么要用这个东西呢？因为它可以帮助我们维护一个完整的python工程，实现零改动的移植。
python开发是有一个不断引入模块的过程，除了python自带的模块之外，很可能会用到第三方模块，这个时候就需要安装这些模块（后面介绍怎么安装）。但是有的时候，第三方模块之间是有冲突的，如果你一股脑都安装到python解释器环境中，会导致在使用了一堆第三方模块之后，继续引入第三方模块的时候出现冲突。或者是你兴冲冲完成了一个艰巨的任务，却发现需要依赖的第三方模块太多太乱了，无法将这个工程单独打包，只能无奈将整个python解释器打包。说了这么多，你就用virtualenv吧^_^
网上有一些介绍安装virtualenv的文章，要求先安装easy_install再用easy_install安装virtualenv。这个顺序其实也没错，不过，virtualenv是完全可以独立安装的，并且也可以反过来，安装virtualenv之后，再到虚拟环境中安装easy_install。不为别的，只为了尽可能少“污染”python解释器的原生环境。
同样，安装virtualenv的方法，请百度之，下载源代码压缩包，解压之后启动一个命令行窗口，cd到对应的解压之后的目录，执行
```
python setup.py install
```
 安装过程输出如下：
```
Note: without Setuptools installed you will have to use "python -m virtualenv ENV"
running install
running build
running build_py
running install_lib
running install_egg_info
Removing D:\Python27\Lib\site-packages\virtualenv-13.1.0-py2.7.egg-info
Writing D:\Python27\Lib\site-packages\virtualenv-13.1.0-py2.7.egg-info
```
第一句话的意思是，未安装setuptools（也就是easy_install）的情况下，使用virtualenv需要执行：python -m virtualenv ENV
ENV是需要创建的环境名。

##### 1.3 easy_install安装
easy_install可以安装到python解释器原生环境中（自行摆渡啊摆渡），也可以安装到virtualenv创建的虚拟环境中。建议安装到虚拟环境中，还是那句话，减少污染，保护环境。
virtualenv 13.1.0版本中自带了setuptools（easy_install），也就是说，创建虚拟环境时，自动在虚拟环境中安装了easy_install。good！
```
D:\>python -m virtualenv testenv
New python executable in testenv\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```
请注意：实际上有三个模块被自动安装到虚拟环境中了，setuptools（easy_install），pip和wheel。实际上它们的功能是相近的，都是安装工具，也是发布工具（我们写的python脚本最终可以发布为一个python模块共享给他人）。有兴趣的同学可以继续百度，这里不再赘述这些工具的优劣，总之我们先用easy_install。
##### 1.4 VC仍然是需要的。
有的python第三方模块是以C/C++源码的形式发布的，此时使用任何安装工具，都会自动调用VC执行该模块的编译，然后才是真正的安装。由此可以看出python其实是有很深的C/C++背景的。不过以后我们会说到，其实python和java也很配，编写jython程序时，有的时候会觉得混乱，因为java和python的语法“混合”起来使用了。
不过对于资深C/C++程序员来说，学习python几乎只需要几天甚至一天的时间即可，没必要看我长篇大论；所以我这个长篇大论是给没有很强的编程知识背景的人看的。但是要这些人玩转VC也有点困难。所以一般我们会绕过这些“开放C/C++源码”的第三方模块，或者找到可以替换的方式来达成这些模块的安装——是的，有更加简单的方式，虽然一般认为这种方式不够通用，但是足够友好，这就够了。
##### 1.5 足够了，开始吧
我们可以先不理会VC的事情，我们已经在1.3中创建了一个python虚拟环境，那么开始我们的第一次python之旅吧
```
C:/> cd /D D:/testenv/Scripts
D:\testenv\Scripts>activate
(testenv) D:\testenv\Scripts>
```
现在我们启动了python虚拟环境，在这个环境中，我们可以执行python解释器了：
```
(testenv) D:\testenv\Scripts>python
Python 2.7.2 (default, Jun 12 2011, 15:08:59) [MSC v.1500 32 bit (Intel)] on win
32
Type "help", "copyright", "credits" or "license" for more information.
>>> print "hello, world!"
hello, world!
>>>
```
## [Python笔记](https://github.com/billy0920/python_tips/blob/master/content.md)
