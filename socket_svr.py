# coding=utf-8
import errno

__author__ = 'Administrator'
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import select


def start():
    """

    
    """
    host = ""
    port = 5001
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(5)
    client_socks = []
    print "begin..."
    while 1:
        infers, outers, errands = select.select([server_sock, ], [], [], 0)
        # 如果infers状态改变,进行处理,否则不予理会
        if len(infers) != 0:
            print "new client"
            clientsock2, clientaddr = server_sock.accept()
            client_socks.append(clientsock2)
            print u"Accept SOCK<{0}>".format(clientsock2)
        if len(client_socks) > 0:
            #epoll
            infds_c, outfds_c, errfds_c = select.select(client_socks, [], client_socks, 0)
            if len(infds_c) != 0:
                for s in infds_c:
                    buf = None
                    try:
                        buf = s.recv(8196)
                    except socket.error as e:
                        if e.errno != errno.EWOULDBLOCK:
                            print "SOCK<{0}> recv error{0}".format(s, e)
                    if buf:
                        print u"buflen={0}".format(len(buf))
                        #print u"SOCK<{0}> Recv[{1}]".format(s, buf)
                    else:
                        print u"SOCK<{0}> is close".format(s)
                        s.close()
                        client_socks.remove(s)

            if len(errfds_c) > 0:
                for s in errfds_c:
                    s.close()
                    if s in client_socks:
                        print u"Close Socket {0}".format(s)
                        client_socks.remove(s)
            # clientsock2.closed()
            #print "client closed"
            #print "no data coming"


if __name__ == "__main__":
    start()
