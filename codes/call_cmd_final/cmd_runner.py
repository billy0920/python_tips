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