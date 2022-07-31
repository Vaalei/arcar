import socket               
 
sock = socket.socket()
 
host = "10.0.0.25" #ESP32 IP in local network
port = 666             #ESP32 Server Port    

message = "hello there!"

sock.connect((host, port))
sock.send(message.encode())
input("Press enter to stop")
sock.close()