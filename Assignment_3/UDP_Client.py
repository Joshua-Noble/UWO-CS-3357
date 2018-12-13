# UDP_Client.py -- A client application for sending packets to a server via UDP with implemented RDT 3.0
# Client will self-terminate after receiving confirmation that all 3 packets reached the server
# Client can be run from command line with no args
# Author: Joshua Noble
# Student #: 250700795

import binascii
import socket
import struct
import sys
import hashlib

# Setup loopback address and ports
UDP_IP = "127.0.0.1"
UDP_PORT_SEND = 12004 # Port for sending packets
UDP_PORT_RECEIVE = 12003 # Port for receiving packets

# Create the socket and bind for listening
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT_RECEIVE))
sock.settimeout(0.009) # 9ms timeout when listening for ACK packets

# Function to calculate and return CheckSum according to ACK, seq number, and packet data
def getCheckSum(ackValue, seqNum, pktData):
    values = (ackValue, seqNum, pktData)
    packer = struct.Struct("I I 8s")
    packed_data = packer.pack(*values)
    chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    return chksum

# Function to send a new packet with relevant information
def sendPacket(ackValue, seqNum, pktData):
    chksum = getCheckSum(ackValue, seqNum, pktData)

    # Build the UDP Packet
    values = (ackValue, seqNum, pktData, chksum)
    UDP_Packet_Data = struct.Struct("I I 8s 32s")
    UDP_Packet = UDP_Packet_Data.pack(*values)

    # Send the UDP Packet
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT_SEND))

    print("Sent packet: ", values)

# Function to listen for and receive packet
def receivePacket(seqNum, pktData):
    try:
        data, addr = sock.recvfrom(1024) # Buffer size is 1024 bytes
        unpacker = struct.Struct("I I 8s 32s")
        UDP_Packet = unpacker.unpack(data)
        print("Received from:", addr)
        print("Received packet:", UDP_Packet)

        result = verifyPacket(UDP_Packet, seqNum)

        return result
    except socket.timeout:
        print("Socket timeout, resending packet")
        return False

# Function to verify CheckSum, Seq Number, and ACK of packet
def verifyPacket(UDP_Packet, seqNum):
    # Create the CheckSum for comparison
    chksum = getCheckSum(UDP_Packet[0], UDP_Packet[1], UDP_Packet[2])

    # Compare CheckSums to test for corrupt data
    if (UDP_Packet[3] == chksum):
        if (UDP_Packet[1] == seqNum): # Verify seq number
            print("CheckSums Match, Sequence # Matches, Packet OK")
            return True
        else:
            print("CheckSums Match, Sequence # Does Not Match, Resending Packet")
    else:
        print("CheckSums Do Not Match, Packet Corrupt, Resending Packet")
    
    return False

# Function that contains the main logic for running the client, called upon running the script
def main():
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT_SEND)
    print("")

    allPktData = (b"NCC-1701", b"NCC-1664", b"NCC-1017") # This is the data of the 3 packets we are trying to send
    ackPktReceived = False
    seqNum = 0

    try:
        for data in allPktData: # Loop through data
            print("------------")
            print("Data: ", data)
            print("------------")
            ackPktReceived = False # Reset ACK confirmation flag when we start to send a packet with new data

            # Loops until we have received the correct ACK confirmation from the server
            while not ackPktReceived:
                sendPacket(0, seqNum, data)
                ackPktReceived = receivePacket(seqNum, data)
                print("------------")

            # Swap seq number before next packet
            seqNum = 1 - seqNum
            print("")
    finally: # Use finally to make sure socket is closed in case of program crash
        sock.close()

main()