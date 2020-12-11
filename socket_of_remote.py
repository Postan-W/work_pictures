#该模块放在远程主机上
import socket
#操作细节参看socket_to_java.py
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 76543
server_socket.bind(("127.0.0.1",port))
