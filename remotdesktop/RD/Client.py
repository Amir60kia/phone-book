import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.16.80.105', 12345))

message = client_socket.recv(1024)
print(message.decode())
client_socket.close()