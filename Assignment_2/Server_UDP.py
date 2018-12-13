# Server_UDP.py -- A server application for receiving packets from a client via UDP
# To stop server while running, please use CTRL+C, or close the running console
# Author: Joshua Noble
# Student #: 250700795

# socket library is used to connect using UDP sockets, datetime library is used for getting current date/time
import socket
import datetime

# Server port number through which packets are received is stored
serverPort = 12469

# Server socket is created, parameters indicate IPv4 (AF_INET) and UDP (SOCK_DGRAM) usage
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server port number is bound to socket, all traffic through specified port will be directed to this socket
serverSocket.bind(("", serverPort))

# Notify user once server is ready to receive packets
print("Server is ready to accept commands")

# Infinite loop to keep server running and listening for connections
while True:
    # Server waits to receive a packet from the client, through server socket (buffer size is 2048)
    # Once received, message is converted from bytes to string, client address is saved for return packet
    message, clientAddress = serverSocket.recvfrom(2048)
    command = message.decode()
    
    # Check if request is a valid command
    if (command == "What is the current date and time?"):
        # Get current date/time and format it to return to client
        currentDT = datetime.datetime.now()
        formattedDT = currentDT.strftime("%m/%d/%Y %H:%M:%S")
        returnMessage = "Current Date and Time - " + formattedDT
        print("Valid request received")
    else:
        # Generate error message to return to client
        returnMessage = "Error, invalid request!"
        print("Invalid request received")
        
    # Client address is attached to return message (once converted to bytes), resulting packet is sent through server socket
    serverSocket.sendto(returnMessage.encode(), clientAddress)
    