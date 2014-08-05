import struct

__author__ = 'Administrator'

import socket, select, os, sys

data_list = []


def do_sth_with_data():
    print '=====Do Sth With Parse Data:======'
    rbuf = data_list.pop()
    parse_recv_data(rbuf, True)
    for i in range(1, len(data_list), 1):
        parse_recv_data(data_list.pop(), False)


def insert_into_data_list(recv_data):
    data_list.append(recv_data)


def get_frame_index(recv_data):
    buf1, fid, buf2, index, buf3 = struct.unpack("4sIsB6s", recv_data)
    return fid, index


def parse_recv_data(recv_data, rflag):
    data_len = 0
    if rflag:
        frame_len, frame_id, check_sum, frame_index, data_len, frame_data = struct.unpack("!2I2BH4s", recv_data)
    else:
        frame_len, frame_id, check_sum, frame_index, frame_data = struct.unpack("!2I2B6s", recv_data)
    print "{0},{1},{2},{3},{4}".format(frame_len, frame_id, check_sum, frame_index, data_len)
    # for i in range(0, 6, 1):
    # print "%c" % frame_data[i]


if __name__ == "__main__":
    # host = "localhost"
    host = "192.168.1.211"
    port = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # mbytestr = '\x80\x08\x00\x00\x12\x34\x56\x78\x11\x22\x33\x44\x55\x66\x77\x88'
    # mbytestr = "test data from client"
    #s.send(mbytestr)
    while 1:
        total_len = 0
        i = 0
        while 1:
            buf = s.recv(1024)
            frame_id, frame_index = get_frame_index(buf)
            print "fid={0},findex={1}".format(frame_id, frame_index)
            if (frame_index == 0) and (i > 0):
                do_sth_with_data()
                insert_into_data_list(buf)
                break
            insert_into_data_list(buf)
            m_len = len(buf)
            total_len += m_len
            i += 1
            print "{0},{1},{2}".format(i, m_len, total_len)
    s.close()