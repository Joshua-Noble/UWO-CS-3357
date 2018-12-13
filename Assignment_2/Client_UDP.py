# Client_UDP.py -- A client application for sending packets to a server via UDP
# Author: Joshua Noble
# Student #: 250700795

# socket library is used to connect using UDP sockets
import socket

# Server address (IPv4) and port number are stored
serverName = "192.168.1.101"
serverPort = 12469

# Client socket is created, parameters indicate IPv4 (AF_INET) and UDP (SOCK_DGRAM) usage
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Message sent to server is given by user via keyboard input
message = input("Input a text command: ")

# Packet is sent to server through UDP socket
# Message must be first converted to bytes (using encode()), then given as a parameter
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Client waits to receive a packet from the server (buffer size is 2048)
serverResponse, serverAddress = clientSocket.recvfrom(2048)

# Response from server is converted from bytes to string and displayed to the user
print(serverResponse.decode())

# Client socket is closed before program ends
clientSocket.close()