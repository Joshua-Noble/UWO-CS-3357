# UDP_Server.py -- A server application for receiving packets from a client via UDP with implemented RDT 2.2
# Server will self-terminate after 15s of socket inactivity
# Server can be run from command line with no args
# Author: Joshua Noble
# Student #: 250700795

import binascii
import socket
import struct
import sys
import hashlib

# Setup loopback address and ports
UDP_IP = "127.0.0.1"
UDP_PORT_RECEIVE = 12004 # Port for receiving packets
UDP_PORT_SEND = 12003 # Port for sending packets

# Create the socket and bind for listening
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT_RECEIVE))
sock.settimeout(15) # Set server timeout to 15s, to make sure server self-terminates after client is done sending data

# Function to calculate and return CheckSum according to ACK, seq number, and packet data
def getCheckSum(ackValue, seqNum, pktData):
    values = (ackValue, seqNum, pktData)
    packer = struct.Struct("I I 8s")
    packed_data = packer.pack(*values)
    chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    return chksum

# Function to send a return packet with confirmation ACK & seq number (data is an empty string for the return packet)
def sendReturnPacket(ackValue, seqNum):
    chksum = getCheckSum(ackValue, seqNum, b"") # Data used in return packet is an empty string, as we do not need to send the actual data back

    # Build the UDP Packet
    values = (ackValue, seqNum, b"", chksum)
    UDP_Packet_Data = struct.Struct("I I 8s 32s")
    UDP_Packet = UDP_Packet_Data.pack(*values)

    # Send the UDP Packet
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT_SEND))

    print("Sent packet: ", values)

# Function that contains the main logic for running the server, called upon running the script
def main():
    try:
        print("Server is ready to receive packets")
        print("")

        # Start with sequence number = 0
        expectedSeq = 0

        # Infinite loop to continue receiving packets until socket times out
        while True:
            # Receive data from client
            data, addr = sock.recvfrom(1024) # Buffer size is 1024 bytes
            unpacker = struct.Struct("I I 8s 32s")
            UDP_Packet = unpacker.unpack(data)

            print("Received from:", addr)
            print("Received packet:", UDP_Packet)

            # Create the CheckSum for comparison
            values = (UDP_Packet[0], UDP_Packet[1], UDP_Packet[2])
            packer = struct.Struct("I I 8s")
            packed_data = packer.pack(*values)
            chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

            # Compare CheckSums to test for corrupt data
            if (UDP_Packet[3] == chksum):
                if (UDP_Packet[1] == expectedSeq): # Verify seq number
                    print("CheckSums Match, Sequence # Matches, Packet OK")

                    # Send return packet with confirmation ACK & seq number
                    sendReturnPacket(1, UDP_Packet[1])

                    # Swap expected seq number before next packet
                    expectedSeq = 1 - expectedSeq
                else:
                    print("CheckSums Match, Sequence # Does Not Match, Resending Packet")

                    # Send return packet with confirmation ACK & seq number
                    sendReturnPacket(1, UDP_Packet[1])
            else:
                print("CheckSums Do Not Match, Packet Corrupt, Resending Packet")

                # Send return packet with non-confirmed ACK & swapped seq number to notify client of packet corruption
                sendReturnPacket(0, (1 - UDP_Packet[1]))
            
            print("")
    except socket.timeout:
        print("Closing socket, max timeout value reached!")
    finally: # Use finally to make sure socket is closed in case of program crash
        sock.close()

main()