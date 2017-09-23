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