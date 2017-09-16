## [Python笔记](https://billy0920.github.io/python_tips)
### 想做就做——python调用外部命令进阶
> 这是全新的篇章。
> 原先的存量文章已经编辑发布完了，现在开始要真正开始写新的文章了。

python调用外部命令，有几种方式：
1. subprocess.Popen
1. os.system
1. os.spawn*
1. os.popen*
1. popen2.*
1. commands.*

有的时候偷懒用os.system，但是实际上subprocess模块的文档中，第一句就是要替换掉其他的调用外部命令的模块。所以如果要学习python调用外部命令，其他的都可以先暂时不用看了，就只看subprocess模块就足够了。

以下介绍subprocess模块调用外部命令的方法：
#### subprocess.call
    subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)

args是一个数组，第一个元素为命令，后面的元素为命令的参数。该方法执行args描述的命令，然后等待命令运行结束，返回命令的返回码（一般的，命令的返回码用于标识命令执行结果是成功还是失败，一般用0表示成功，用非0表示失败）。

* 警告：设置shell=True可能导致安全问题。

* 注意：这里不能设置stdout=PIPE或者stderr=PIPE，否则会导致程序被阻塞。

#### subprocess.check_call
    subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
跟subprocess.call类似，区别在于如果命令返回非0，则抛出CalledProcessError异常。

#### subprocess.check_output
    subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)

跟subprocess.check_call类似，区别在于命令返回0时，返回的值是命令的标准输出字符串（命令显示在命令行的内容）。

#### subprocess.Popen
    subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

subprocess.Popen并不是一个简单的函数，而是一个类。在初始化该类的实例的时候，会启动一个进程去执行args描述的命令（以及参数），然后返回Popen类的一个实例（初始化类，肯定是返回类的实例啊）。然后可以使用这个返回的类实例，进一步与该命令对应的进程进行交互。
最基本的例子如下：
```python
import subprocess

def example1():
    p = subprocess.Popen(["dir"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    ret_code = p.returncode
    print "return code == ",ret_code
    print "stdout:", out
    print "stderr:", err
```
这个例子中，第一个参数指明要调用dir命令（windows环境），第二个参数指定需要获取标准输出，第三个参数指定需要获取错误输出，第四个参数指定用通过系统shell运行该命令（这里，如果设置shell=False，则会抛出异常WindowsError: [Error 2] ，表示找不到该命令）。

通过调用p.communicate()，我们可以得到该进程的标准输出和错误输出。当然这个命令在windows上运行的时候不会报错，因此只有标准输出返回了字符串，错误输出返回空字符串，返回码为0。该方法的定义为：Popen.communicate(input=None)，其中可以提供一个参数值input，表示提供给该命令运行进程的<b>一次</b>输入，比如比较常见的某些命令需要回答y/n的时候，可以通过Popen.communicate("y")来回答，以便命令继续运行。

通过这个最基本的调用方式，可以满足最多交互一次的命令的调用。

但是，对于类似ftp等工具命令来说，这样的程度是远远不够的。调用ftp命令，需要使用一些列的交互操作来完成一次文件传输，因此不能直接用以上的例子来调用ftp命令，而是需要提供多次交互的能力。

```python
from subprocess import *

def example2():
    proc = Popen(['ftp', "127.0.0.1"],stdin=PIPE,stdout=PIPE,shell=False)
    cmds = ["ftp_username", "passwd", "pwd", "quit"]
    for line in cmds:
        proc.stdin.write("%s\r\n"%line)
        proc.stdin.flush()
        output = proc.stdout.readline()
        print(output)
```

这个例子展示了subprocess.Popen多次交互的能力，首先执行命令```ftp 127.0.0.1```打开一个ftp会话，然后输入用户名```ftp_username```和密码```passwd```，登录之后，再执行pwd显示当前路径（当然也可以执行其他的命令了），然后退出。

* 这个例子需要有一个ftpserver配合执行，否则打开ftp会话的时候就报错无法执行下去了。

通过以上的例子，可以看到我们成功地执行了多次交互命令。具备了这样的能力之后，我们几乎可以操作任意的命令工具了。

当然这个例子还需要继续改进，比如针对每一次交互的显示，决定下一步应该输入什么内容，或者出错需要终止交互。

细心的人或许就会发现，这里的shell=False，为什么？这个问题很好，在我所经历的涉及命令调用的项目中，就遇到过很多命令，必须设置shell=True或者shell=False才能够正确执行，否则就根本无从调用，甚至在windows中必须设置shell=False而在linux中必须设置shell=True。当然对于程序员来说，这些都是能做到的，无非就是多几个判断语句而已。

但是这样适配，意味着写出来的代码很难做到平台无关，设置我怀疑在win7中运行正常的代码，在win2008server中可能无法正确运行。

经历了无数次糟心之后，我终于找到了一个一次性解决这类问题的终极方案，那就是[《想做就做——调用外部命令终极篇》](https://billy0920.github.io/python_tips)

## [Python笔记](https://billy0920.github.io/python_tips)
