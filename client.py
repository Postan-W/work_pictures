#该模块连接对方的socket，作用是将拉取的图片传过去然后去logo
import sys
import struct
import socket
import os

def sock_client_image(imagepath,topic:str='0'):
    '''
    :param topic: str --> only '0' or '1'
    0是排行图片，1是素材洞察
    '''

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.128.12.15',8101))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    fhead = struct.pack(b'128sq', bytes(os.path.basename(imagepath)+topic, encoding='utf-8'),
                        os.stat(imagepath).st_size)  # 将xxx.jpg以128sq的格式打包

    s.send(fhead)

    fp = open(imagepath, 'rb')  # 打开要传输的图片
    while True:
        data = fp.read(1024)  # 读入图片数据
        if not data:
            print('{0} send success,please waiting...'.format(imagepath))
            break
        s.send(data)  # 以二进制格式发送图片数据
    s.send(b'1')
    print(s.recv(1024).decode())
    s.close()
            # break    #循环发送