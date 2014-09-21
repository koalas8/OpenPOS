# -*- coding=utf-8
import socket
from ccard.protocols.trans import Trans_pb2

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host = 'localhost'
port = 8003

trans = Trans_pb2.Trans()
trans.action = 'singin'
trans.shop_no = '12'
trans.terminal_no = '56'

def test():
    s.connect((host, port))
    s.send(trans.SerializeToString())
    s.close()

if __name__ == '__main__':
    test()
