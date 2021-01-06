import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.56.1",54321))
#发送数据
with open("a60.jpg","rb") as f:
    #client.send("该信息由python客户端发出........".encode())
    #字节流长度
    #length = len(f.read())
    #client.send(str(length).encode('utf-8'))
    client.send(f.read())
#接收数据
#print(client.recv(1024*1024*500).decode('utf-8'))
#接收字节流
receive = client.recv(1024)