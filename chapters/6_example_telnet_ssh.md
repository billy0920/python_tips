## [Python笔记](https://billy0920.github.io/python_tips)

### 想做就做——telnet与ssh命令行工具篇

Telnet和SSH是各类服务器或者网络设备一般会支持的交互方式。对于服务器维护人员或者网络设备管理员，有一个功能强大的Telnet/SSH客户端，往往事半功倍。

Telnet和SSH也能让我们更加深入的了解网络交互，甚至Telnet在某种形式上可以取代浏览器去获取网页内容。因此，学习Telnet和SSH客户端的实例，进而为写出更强大的网络软件打下基础。建议好好学习本例。

python自带一个telnetlib模块，支持基本的telnet操作。但是对于一般的telnet服务器来说，还要至少支持VT100等虚拟终端协议。因此需要进行一些必要的改进。

python有原生的ssh操作模块，但是使用起来比较复杂。可以通过安装一个第三方的paramiko模块来支持ssh操作。

python通过调用telnet或者ssh，可以做到对所有的命令行程序的调用，支持程序内的多次交互。

#### 1.在虚拟环境中安装paramiko。
因为虚拟环境中已经缺省安装了easy_install工具，因此安装paramiko貌似非常简单（虚拟环境假设安装在D:/testenv），以下是命令行激活虚拟环境和安装paramiko的过程：

```bat
D:\testenv\Scripts>activate
(testenv) D:\testenv\Scripts>easy_install paramiko
Searching for paramiko
Reading https://pypi.python.org/simple/paramiko/
Best match: paramiko 1.15.2
Downloading https://pypi.python.org/packages/source/p/paramiko/paramiko-1.15.2.t
ar.gz#md5=6bbfb328fe816c3d3652ba6528cc8b4c
Processing paramiko-1.15.2.tar.gz
Writing c:\users\admini~1\appdata\local\temp\easy_install-sflvco\paramiko-1.15.2
\setup.cfg
Running paramiko-1.15.2\setup.py -q bdist_egg --dist-dir c:\users\admini~1\appda
ta\local\temp\easy_install-sflvco\paramiko-1.15.2\egg-dist-tmp-smkdeg
warning: no files found matching 'user_rsa_key' under directory 'demos'
warning: no files found matching 'user_rsa_key.pub' under directory 'demos'
zip_safe flag not set; analyzing archive contents...
Moving paramiko-1.15.2-py2.7.egg to d:\testenv\lib\site-packages
Adding paramiko 1.15.2 to easy-install.pth file
Installed d:\testenv\lib\site-packages\paramiko-1.15.2-py2.7.egg
Processing dependencies for paramiko
Searching for ecdsa>=0.11
Reading https://pypi.python.org/simple/ecdsa/
Best match: ecdsa 0.13
Downloading https://pypi.python.org/packages/source/e/ecdsa/ecdsa-0.13.tar.gz#md
5=1f60eda9cb5c46722856db41a3ae6670
Processing ecdsa-0.13.tar.gz
Writing c:\users\admini~1\appdata\local\temp\easy_install-3n4kxd\ecdsa-0.13\setu
p.cfg
Running ecdsa-0.13\setup.py -q bdist_egg --dist-dir c:\users\admini~1\appdata\lo
cal\temp\easy_install-3n4kxd\ecdsa-0.13\egg-dist-tmp-l2wsr7
zip_safe flag not set; analyzing archive contents...
Moving ecdsa-0.13-py2.7.egg to d:\testenv\lib\site-packages
Adding ecdsa 0.13 to easy-install.pth file
Installed d:\testenv\lib\site-packages\ecdsa-0.13-py2.7.egg
Searching for pycrypto!=2.4,>=2.1
Reading https://pypi.python.org/simple/pycrypto/
Best match: pycrypto 2.6.1
Downloading https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.1.ta
r.gz#md5=55a61a054aa66812daf5161a0d5d7eda
Processing pycrypto-2.6.1.tar.gz
Writing c:\users\admini~1\appdata\local\temp\easy_install-efndl1\pycrypto-2.6.1\
setup.cfg
Running pycrypto-2.6.1\setup.py -q bdist_egg --dist-dir c:\users\admini~1\appdat
a\local\temp\easy_install-efndl1\pycrypto-2.6.1\egg-dist-tmp-qvm88o
warning: GMP or MPIR library not found; Not building Crypto.PublicKey._fastmath.
error: Setup script exited with error: Microsoft Visual C++ 9.0 is required (Una
ble to find vcvarsall.bat). Get it from http://aka.ms/vcpython27
(testenv) D:\testenv\Scripts>
```

使用easy_install安装的时候，如果没有明确指定版本，easy_install会选择一个最新的版本，并且如果该模块依赖其他的模块的话，会自动下载安装。多美好啊~

然而，好与不好是共存的。从安装的过程信息我们看到，paramiko还依赖于ecdsa和pycrypto，并且ecdsa模块被正常安装了（嗯，没报错就是成功），但是pycrypto没有安装成功，报错信息是说需要VC9.0，推测pycrypto的源码中包含了C/C++，需要使用VC执行编译。WTF~！

理论上如果本机也安装了VC9.0，就可以一个命令完全安装paramiko和它的依赖模块ecdsa和pycrypto了。然而不要想得太简单，这里说能完全安装paramiko，实际上是需要调用VC编译paramiko的依赖模块pycrypto，VC编译时可能会有其他的错误，然后无限递归下去。这里只是举一个例子，其实编译pycrypto没有那么复杂，但是如果是其他的模块呢？总之，复杂的事情会有很多。

怎么解决这样的问题呢？

* 下载相应模块的.msi文件来安装会更直接一些。一般来说，总是能搜索找到python模块的.msi或者.exe的windows安装程序的^_^

我们在[http://www.voidspace.org.uk/python/modules.shtml#pycrypto]找到了windows安装程序，下载之后缺省安装，由于安装程序会查找注册表，安装的python模块就会被安装到python原生环境中，会污染原生的python环境。不过我们只是要安装后的文件就足够了。安装pycrypto的过程就不截图了。

安装结束之后，查看python原生环境的根目录，会发现多了两个文件：```pycrypto-wininst.log```和```Removepycrypto.exe```。顾名思义，```Removepycrypto.exe```就是用来卸载pycrypto模块的。而```pycrypto-wininst.log```则是对应的安装日志，貌似卸载程序会根据这个日志去查找安装的文件并删除掉，反过来说，我们可以根据这个文件找到安装程序产生的文件，将这些文件拷贝到虚拟环境中，就相当于手工安装了这个模块。

查看```pycrypto-wininst.log```日志内容，发现安装程序实际上就是在python原生环境的Lib\site-packages中生成了pycrypto-2.6-py2.7.egg-info文件和一个文件夹Crypto，然后拷贝了多个文件到Crypto文件夹中。因此我们只需要将pycrypto-2.6-py2.7.egg-info文件和文件夹Crypto拷贝到虚拟环境中对应的Lib目录下就可以了。

手工拷贝了pycrypto模块的相关文件之后，再到虚拟环境中启动安装paramiko，输出如下：
```bat
(testenv) C:\Users\Administrator\Downloads>easy_install paramiko
Searching for paramiko
Best match: paramiko 1.15.2
Processing paramiko-1.15.2-py2.7.egg
paramiko 1.15.2 is already the active version in easy-install.pth
Using d:\testenv\lib\site-packages\paramiko-1.15.2-py2.7.egg
Processing dependencies for paramiko
Finished processing dependencies for paramiko
(testenv) C:\Users\Administrator\Downloads>
```
这里ecdsa在之前已经安装了，pycrypto也被我们手工安装了，因此已经不需要再安装这两个模块了。

启动python试试看：
```bat
(testenv) C:\Users\Administrator\Downloads>python
Python 2.7.2 (default, Jun 12 2011, 15:08:59) [MSC v.1500 32 bit (Intel)] on win
32
Type "help", "copyright", "credits" or "license" for more information.
>>> import paramiko
>>> dir(paramiko)
['AUTH_FAILED', 'AUTH_PARTIALLY_SUCCESSFUL', 'AUTH_SUCCESSFUL', 'Agent', 'AgentK
ey', 'AuthHandler', 'AuthenticationException', 'AutoAddPolicy', 'BadAuthenticati
onType', 'BadHostKeyException', 'BaseSFTP', 'BufferedFile', 'Channel', 'ChannelE
xception', 'ChannelFile', 'DSSKey', 'ECDSAKey', 'GSSAuth', 'GSS_AUTH_AVAILABLE',
'HostKeys', 'InteractiveQuery', 'Message', 'MissingHostKeyPolicy', 'OPEN_FAILED
_ADMINISTRATIVELY_PROHIBITED', 'OPEN_FAILED_CONNECT_FAILED', 'OPEN_FAILED_RESOUR
CE_SHORTAGE', 'OPEN_FAILED_UNKNOWN_CHANNEL_TYPE', 'OPEN_SUCCEEDED', 'PKey', 'Pac
ketizer', 'PasswordRequiredException', 'ProxyCommand', 'ProxyCommandFailure', 'R
SAKey', 'RejectPolicy', 'SFTP', 'SFTPAttributes', 'SFTPClient', 'SFTPError', 'SF
TPFile', 'SFTPHandle', 'SFTPServer', 'SFTPServerInterface', 'SFTP_BAD_MESSAGE',
'SFTP_CONNECTION_LOST', 'SFTP_EOF', 'SFTP_FAILURE', 'SFTP_NO_CONNECTION', 'SFTP_
NO_SUCH_FILE', 'SFTP_OK', 'SFTP_OP_UNSUPPORTED', 'SFTP_PERMISSION_DENIED', 'SSHC
lient', 'SSHConfig', 'SSHException', 'SecurityOptions', 'ServerInterface', 'Subs
ystemHandler', 'Transport', 'WarningPolicy', '__all__', '__author__', '__builtin
s__', '__doc__', '__file__', '__license__', '__loader__', '__name__', '__package
__', '__path__', '__version__', '__version_info__', '_version', 'agent', 'auth_h
andler', 'ber', 'buffered_pipe', 'channel', 'client', 'common', 'compress', 'con
fig', 'dsskey', 'ecdsakey', 'file', 'hostkeys', 'io_sleep', 'kex_gex', 'kex_grou
p1', 'kex_group14', 'kex_gss', 'message', 'packet', 'pipe', 'pkey', 'primes', 'p
roxy', 'py3compat', 'resource', 'rsakey', 'server', 'sftp', 'sftp_attr', 'sftp_c
lient', 'sftp_file', 'sftp_handle', 'sftp_server', 'sftp_si', 'ssh_exception', '
ssh_gss', 'sys', 'transport', 'util']
>>>
```

看到了吧，已经可以使用paramiko模块了。paramiko模块提供了 SSHClient，实际上已经可以很方便到地模拟SSH客户端操作了。我们要做的，只是做一些封装。

这个安装过程比较啰嗦，但是至此一次，后面我们安装其他第三方模块的时候，就参照这个过程，不需要多说了。

#### 2.开始编写命令行工具。

如果只支持telnet命令行，是不需要安装paramiko的，但是相信我，你学习了paramiko的安装过程方法，以后安装其他模块时总会用得到的。 

python自带了telnetlib模块，支持原始的telnet操作。但是它如此原始，我们需要自行定义虚拟终端（VT）命令交互的部分内容，这样才能愉快地与一般的telnet服务器交互。

telnet是一个应用层协议，是internet开始发展起来时，一个用于远程网络访问的协议。很多软件设计都有相似的情况，那就是，一旦一个早期的设计被实现，只要这个设计还算过得去，就会一直被使用、被继承，继而很长一段时间里，大量的产品都不得不支持它，最终它就一直存活下去，尽管可能有很多让人诟病的地方。尽管后来出现了很多更好的远程访问方式，但是telnet一直被大量的产品支持，而且还将继续被使用下去，尽管它很不安全。

最原始的telnet客户端的实例代码如下：
```python
import getpass
import sys
import telnetlib

HOST = "localhost"
user = raw_input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("ls\n")
tn.write("exit\n")

print tn.read_all()
```

不要怪我偷懒啊，这个python帮助文档中的例子其实是非常好的，一定要认真学习。

这个例子相当的原始，以至于还没有体现人机交互，仅仅只是建立一个到目的主机的Telnet连接，然后等待，直到接收到"login: "字符串，然后就发送用户名，接着继续等待，直到接收到"Password: "字符串，继续输入密码，然后执行ls命令，接着执行exit命令，最后退出。脚本中的HOST的值为"localhost"，如果本机安装了telnet server，启动telnet server之后就可以运行该脚本，查看结果。如果没有安装telnet server，可以修改HOST为一个已知的提供telnet server的主机名或者IP，例如各大高校的BBS，一般都会提供telnet服务。

如果你真的听我的建议，用以上的脚本去链接高校BBS，就会发现可能长时间无响应，因为预期接收的"login :"字符串可能没有出现，请将预期接收的字符串修改为":"，这样就很容易满足条件，进而看到接收的数据。一般的，我们会接收到了很多的“乱码”。形如：
```
[31m欢迎光临[1;40;33m [m[[0;1;33;45m Add '.' after YourID to login for BIG5 [m]
```
这些"乱码"有一个规律，就是以左中括号"["开始，以字母"m"结束。这个其实是所谓的虚拟终端的控制字符。所谓的虚拟终端，又牵扯出很多内容，我们只关注一件事情，那就是虚拟终端可以在Telnet中展示非常丰富的内容，而这些内容基本上都是通过类似的控制字符实现的：```"["+xxx+"m"```。我们现在暂时还不需要去理解它们，只是为了显示内容，我们需要去除掉这些多余的字符。假定我们接收到的数据为data，那么过滤掉虚拟终端控制字符的函数可以这样写：
```python
import re
text = tn.read_all()
re.sub(r"\[[^\]*m","",text)
```
## [Python笔记](https://billy0920.github.io/python_tips)
