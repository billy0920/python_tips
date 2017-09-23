## [Python笔记](https://billy0920.github.io/python_tips)
### 想做就做——python调用外部命令终极篇
> 这是一篇关于python调用外部命令的终极方案。

在[《想做就做——python调用外部命令进阶》](https://billy0920.github.io/python_tips/chapters/7_example_call_command_advanced)中有个问题，就是调用外部命令的```subprocess.Popen```中有一个shell参数，不但带来安全问题，而且针对某些命令，必须设置```shell=True```，而另一些命令，则必须设置```shell=False```，否则无法正常调用；甚至有些命令，在windows环境上需要设置```shell=True```，而在linux上则需要设置```shell=False```，不同的平台需要用不同的代码去适配才能正常运行。

不单是shell参数的问题，实际上，调用外部命令还存在诸多的限制，多次交互时交互方式的不一致，等等的问题会导致看起来很简单的外部命令调用变得非常复杂。

> 有没有比较好的解决方案呢？

> 答案是：有！

这就是本篇的关键内容，一个统一的python调用外部命令的解决方案。

<b>通过SSH/TELNET登录到本地的SSH/TELNET server，然后执行外部命令调用。</b>

TELNET [cmd server](https://billy0920.github.io/python_tips/codes/call_cmd_final/cmd_server.py)的实现代码如下：
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

执行命令的[cmd runner](https://billy0920.github.io/python_tips/codes/call_cmd_final/cmd_runner.py)如下:

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


## [Python笔记](https://billy0920.github.io/python_tips)
