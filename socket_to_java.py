import socket
import sys
import threading
import json
import numpy as np
import struct
#创建服务器套接字
#socket.socket(socket_family,socket_type,protocol=0)
"""
socket_family可以是如下参数：

　　socket.AF_INET IPv4（默认）

　　socket.AF_INET6 IPv6

　　socket.AF_UNIX 只能够用于单一的Unix系统进程间通信
"""
"""
socket_type可以是如下参数:

　　socket.SOCK_STREAM　　流式socket , for TCP （默认）

　　socket.SOCK_DGRAM　　 数据报式socket , for UDP

　　socket.SOCK_RAW 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。

　　socket.SOCK_RDM 是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。

　　socket.SOCK_SEQPACKET 可靠的连续数据包服务
"""
"""
protocol参数：

　　0　　（默认）与特定的地址家族相关的协议,如果是 0 ，则系统就会根据地址格式和套接类别,自动选择一个合适的协议
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
print("服务主机名："+hostname)
ip_address = socket.gethostbyname(hostname)
print("ip地址是："+ip_address)
#设置端口
port = 54321
#将套接字和本地主机与端口绑定
server_socket.bind((hostname,port))
# 设置监听最大连接数
server_socket.listen(5)
# 获取本地服务器的连接信息
socket_name = server_socket.getsockname()
print(socket_name)

class ServerThreading(threading.Thread):
    # words = text2vec.load_lexicon()
    def __init__(self, clientsocket,recvsize=1024 * 1024*3,encoding="utf-8"):
        #以上参数为客户端的连接、缓冲区大小(一次接收的数据量，放到内存中),数据编码
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        self.count = 0


    def run(self):
        print("开启线程.....")
        try:
            #定义文件头

            rec = self._socket.recv(self._recvsize)
            self.count += 1
            print(self.count)
            with open("new_a60.jpg","wb") as f:
                f.write(rec)
           # print(type(rec))

            sendmsg = "接收的数据已经过python处理"
            # 发送数据
            self._socket.send(("%s\n" % sendmsg).encode(self._encoding))
            self._socket.send(("这是由python返回的第二条数据").encode(self._encoding))
        except Exception as identifier:
            self._socket.send("接收与处理数据发生错误！！！！".encode(self._encoding))
            print(identifier)
        finally:
            self._socket.close()
        print("本次任务结束.....")

    def __del__(self):
        pass

while True:
    # 获取一个客户端连接
    clientsocket,addr = server_socket.accept()#接到客户端请求前就卡在这里
    print("连接地址:%s" % str(addr))
    #接到请求后创建一个线程处理
    try:
        t = ServerThreading(clientsocket)  # 为每一个请求开启一个处理线程
        t.start()

    except Exception as identifier:
        print(identifier)

server_socket.close()


