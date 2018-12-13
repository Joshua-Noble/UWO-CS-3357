# Client_TCP.py -- A client application for sending packets to a server via TCP
# Author: Joshua Noble
# Student #: 250700795

# socket library is used to connect using TCP sockets
import socket

# Server address (IPv4) and port number are stored
serverName = "192.168.1.101"
serverPort = 12000

# Client socket is created, parameters indicate IPv4 (AF_INET) and TCP (SOCK_STREAM) usage
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connection request sent to server through specified port
clientSocket.connect((serverName, serverPort))

# Message sent to server is given by user via keyboard input
message = input("Input a text command: ")

# Packet is sent to server through open TCP socket
# Message must be first converted to bytes (using encode()), then given as a parameter
clientSocket.send(message.encode())

# Client waits to receive a packet from the server (buffer size is 2048)
serverResponse = clientSocket.recv(2048)

# Response from server is converted from bytes to string and displayed to the user
print(serverResponse.decode())

# Client socket is closed before program ends
clientSocket.close()