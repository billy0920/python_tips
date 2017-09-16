## [Python笔记](https://billy0920.github.io/python_tips)

### 想做就做——python的胶水特性，简单调用操作系统命令和外部程序

python调用操作系统命令和外部程序非常简单，并且能够获取调用的返回值和输出（标准输出和错误输出），这使得用python作为胶水语言，拼接一整套工具成为很方便的事情。

代码先行：
```python
from subprocess import *
import os

def example1():
    p = Popen(["dir"], stdout=PIPE, stderr=PIPE, shell=True)
    b,c = p.communicate()
    a = p.returncode
    print "return code == ",a
    print "stdout:", b
    print "stderr:", c

def example2():
    print os.system("dir")
```

python调用操作系统命令和外部程序有很多方式，但是比较好用的有两种：一是使用subprocess模块，调用subprocess模块的Popen函数，通过设置stdout和stderr参数，可以得到调用的输出和错误信息。二是使用os模块的system函数，这种调用方式只能得到返回码。

这里详细介绍一下subprocess的Popen函数的使用。该函数的格式为：<code>Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)</code>，其中：

<b>args</b>：这是一个list，第一个元素为命令或者外部程序名，第二个参数及后面的参数作为该命令或者程序的参数。例如：["dir", "/S"]，相当于在命令行中执行：

```C:\>dir /S```

<b>stdin</b>：表示后面还需要再给这个命令或者程序执行一次输入，如果要给出参数值，必须是stdin=PIPE或者一个可读文件句柄；

<b>stdout</b>：表示执行结束之后要获取执行的标准输出，如果要给出参数值，必须是stdout=PIPE或者一个可写文件句柄；

<b>stderr</b>：类似于stdout，只是这个用于获取执行的错误结果输出（例如C++程序中用cerr输出的内容）；

<b>shell</b>：表示是否用shell执行。这个其实会让人很迷惑。不过不要紧，你只要记住：如果缺省情况下执行程序出错或者无响应，请使用shell参数，尝试shell=True或者shell=False。

<b>cwd</b>：执行命令或者程序时需要预先进入的路径。例如有些程序的执行是跟当前路径相关的，此时需要指定这个路径，相当于执行命令之前，执行了以下命令：

windows: ```cd /D cwd```

linux:```cd cwd```

<b>env</b>：缺省情况下，操作系统的环境变量会为操作系统命令和外部程序提供执行环境。但是在某些情况下，比如一些绿色程序，它们未注册到操作系统环境变量中，因为无法直接调用，此时可以通过提供env，让python找到这个程序，并顺利调用执行。例如，你解压了一个jre包，但是未将jre解压路径的bin目录路径加入到操作系统的Path变量中，此时，你是无法通过Popen调用java的。这个时候，你可以构造一个env参数：
```python
ENV = os.environ
ENV["Path"] = ENV["Path"]+";"+"C:/jre/bin"
```
然后将此ENV作为env参数传递给Popen，在Popen中就可以直接调用java程序了。

其他参数这里就不详细介绍了，但是以上介绍的参数已经足够你非常好的运用Popen去调用操作系统命令和外部程序了。

可以看到，作为胶水语言调用操作系统命令和外部程序，对操作系统命令和外部程序是有一定的限制的，那就是：执行命令行，能够在命令行返回标准输出和错误输出，并且只能简单地交互（目前只支持一次交互输入。 * <b>错误！</b> 其实是可以支持多次交互的，但是不能简单地使用communicate()函数，请参考[《想做就做——python调用外部命令进阶》](https://billy0920.github.io/python_tips/chapters/7_example_call_command_advanced)）。

例如操作系统的ftp程序，在调用的时候除了支持参数输入远程主机和用户名密码（用户名密码有的也不支持参数输入），然后还需要输入cd命令、get命令、set命令等以完成一次完整的ftp传输操作，因此并不适合于简单的Popen调用。对于这种情况，只能用其他的支持所有操作参数化的ftp工具来完成。不过也有另外的办法，在[《telnet与ssh命令行工具篇》](https://billy0920.github.io/python_tips/chapters/6_example_telnet_ssh)进行介绍。

## [Python笔记](https://billy0920.github.io/python_tips)
