# Server_TCP.py -- A server application for receiving packets from a client via TCP
# To stop server while running, please use CTRL+C, or close the running console
# Author: Joshua Noble
# Student #: 250700795

# socket library is used to connect using TCP sockets, datetime library is used for getting current date/time
import socket
import datetime

# Server port number through which packets are received is stored
serverPort = 12000

# Server socket is created, parameters indicate IPv4 (AF_INET) and TCP (SOCK_STREAM) usage
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server port number is bound to socket, all traffic through specified port will be directed to this socket
serverSocket.bind(("", serverPort))

# Server listens for TCP connection requests from client (max number of queued connections is 1)
serverSocket.listen(1)

# Notify user once server is ready to accept connections
print("Server is ready to accept connections\n")

# Infinite loop to keep server running and listening for connections
while True:
    # Server waits for client to establish initial connection, before opening connectionSocket 
    connectionSocket, addr = serverSocket.accept()
    
    print("------------------------")
    print("Connection socket opened\n")
    
    # All packets will be received through the newly opened connection socket
    # Once received, message is converted from bytes to string
    command = connectionSocket.recv(2048).decode()
    
    # Check if request is a valid command
    if (command == "What is the current date and time?"):
        # Get current date/time and format it to return to client
        currentDT = datetime.datetime.now()
        formattedDT = currentDT.strftime("%m/%d/%Y %H:%M:%S")
        returnMessage = "Current Date and Time - " + formattedDT
        
        print("Valid request received\n")
    else:
        # Generate error message to return to client
        returnMessage = "Error: invalid request!"
        
        print("Invalid request received\n")
        
    # Return message is sent through existing open connection socket (once converted to bytes)
    connectionSocket.send(returnMessage.encode())
    
    # Connection socket is closed before listening for a new connection
    connectionSocket.close()
    
    print("Connection socket closed")
    print("------------------------\n")
    