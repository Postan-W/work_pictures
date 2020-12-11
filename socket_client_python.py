import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((('140.210.92.100',10111)))
client.send("该信息由python客户端发出........".encode())
print(client.recv(1024).decode('utf-8'))