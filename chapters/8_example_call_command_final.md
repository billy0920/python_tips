## [Python笔记](https://billy0920.github.io/python_tips)
### 想做就做——python调用外部命令终极篇
> 这是一篇关于python调用外部命令的终极方案。

在[《想做就做——python调用外部命令进阶》](https://billy0920.github.io/python_tips/chapters/7_example_call_command_advanced)中有个问题，就是调用外部命令的```subprocess.Popen```中有一个shell参数，不但带来安全问题，而且针对某些命令，必须设置```shell=True```，而另一些命令，则必须设置```shell=False```，否则无法正常调用；甚至有些命令，在windows环境上需要设置```shell=True```，而在linux上则需要设置```shell=False```，不同的平台需要用不同的代码去适配才能正常运行。

不单是shell参数的问题，实际上，调用外部命令还存在诸多的限制，多次交互时交互方式的不一致，等等的问题会导致看起来很简单的外部命令调用变得非常复杂。

> 有没有比较好的解决方案呢？

> 答案是：有！

这就是本篇的关键内容，一个统一的python调用外部命令的解决方案。

<b>通过SSH/TELNET登录到本地的SSH/TELNET server，然后执行外部命令调用。</b>

对于windows，可以启动windows本身的TELNET服务，也可以通过软件安装一个TELNET服务。不过既然已经学了python，可以用python实现一个TELNET服务， [cmd server](https://billy0920.github.io/python_tips/codes/call_cmd_final/cmd_server.py)的实现代码如下：
```python
import sys
import subprocess
import threading
import socket


def read_input(client, shell, address):
    f = client.makefile()
    try:
        while True:
            cmd = f.readline()
            shell.stdin.write("%s\r\n" % cmd)

    except IOError, e:
        print "%s exit." % str(address)
    finally:
        client.close()


def send_output(client, shell):
    try:
        while True:
            ret = shell.stdout.readline()
            client.sendall(ret)

    except:
        pass


def send_err(client, shell):
    try:
        while True:
            ret = shell.stderr.readline()
            client.sendall(ret)

    except:
        pass


def deal_with_request(client, address):
    print "%s enter." % str(address)
    shell = subprocess.Popen(["cmd"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    threading.Thread(target=read_input, args=(client, shell, address)).start()
    threading.Thread(target=send_output, args=(client, shell)).start()
    threading.Thread(target=send_err, args=(client, shell)).start()


def main():
    args = sys.argv
    print args
    HOST, PORT = "localhost", 9999
    if len(args) == 2:
        HOST, PORT = args[1], 9999
    elif len(args) >= 3:
        HOST, PORT = args[1], int(args[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (HOST, PORT)
    sock.bind(address)
    print "listening on %s:%s" % address
    sock.listen(50)
    while True:
        client,address = sock.accept()
        thread = threading.Thread(target=deal_with_request, args=(client, address))
        thread.start()


if __name__ == "__main__":
    main()

```

用于执行命令的[cmd runner](https://billy0920.github.io/python_tips/codes/call_cmd_final/cmd_runner.py)如下:

```python
import socket


def run_cmd(cmd, expected):
    HOST, PORT = "localhost", 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        sock.recv(65535)
        received = ""
        sock.sendall("%s\r\n" % cmd)
        while True:
            received += sock.recv(65535)
            if expected in received:
                break
    finally:
        sock.close()

    print "cmd: %s" % cmd
    print "response: %s" % received



if __name__ == "__main__":
    run_cmd("dir", ">\r\n")
    run_cmd("help", ">\r\n")
```

当然，以上的执行命令的代码，可以i非常容易地扩展。通过这样的方式实现外部命令调用，因为TELNET服务是在本地，通过网络连接之后，执行的命令也相当于是在本地执行，并且在一个连接中执行的命令还可以共用同一个运行环境，上一个命令遗留的环境信息，可以给下一个命令使用。

同时，调用外部命令的很多问题都被“远程执行”给屏蔽掉了，不管原先是需要设置shell=True还是shell=False的命令，都是一样的调用方式。

但是，这里也带来另外的问题：命令的执行返回码无法直接返回。因为远程执行的命令虽然有返回码，但是除非显式地用特殊命令格式保存下来，否则返回码就丢失了。这里可以在调用的时候，统一将命令封装成获取返回码的格式。这又是另外一篇文章了。

对于linux来说，一般自身就带有TELNET服务和SSH服务，不过考虑到网络安全的问题，一般只启动SSH，不启动TELNET服务。SSH的远程执行，可以使用paramiko实现的SSH客户端API去调用执行。

## [Python笔记](https://billy0920.github.io/python_tips)
