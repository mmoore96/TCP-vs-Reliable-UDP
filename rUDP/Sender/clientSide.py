import socket
from datetime import datetime, time
import time
import threading
import filecmp
import os
eof = "-1".encode('utf8')
import hashlib
#initializing host, port, filename, total time and number of times to send the file
serverAddress = '000.000.0.00' #PUT the Server IP HERE!
serverPort = 10002
fileName = "send.txt"
totalTime = 0

#change depending on how many files you will be sending
numTimesSend = 20
seqNum = 30000
bytesData = seqNum.to_bytes(5,"little")
print('I am connecting to server side: ', serverAddress,'\n')
#using a for loop to send the file num times
timeToStart = 0
bufferSize = 8192
for x in range(numTimesSend):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (serverAddress, serverPort)
    fileName = "send.txt"
    statinfo = os.stat(fileName)
    print('I am sending file', fileName,' for the ',x + 1,'th  time')
    #opening file to read
    file_to_send = open(fileName, 'rb')
    fileData = file_to_send.read(bufferSize - 5)
    data = bytesData + fileData
    packetsToSend = statinfo.st_size / bufferSize
    startTime = datetime.now()
    start_time = time.time()
    while timeToStart == 0:
            sTime = datetime.now()
            s_time = time.time()
            timeToStart = 1
    for j in range (int(packetsToSend) + 1):

        try:
            sock.settimeout(0.600)
            sent = sock.sendto(data, server_address)
        except socket.timeout:
            sent = sock.sendto(data, server_address)
        try:
            sock.settimeout(2)
            adk, server = sock.recvfrom(bufferSize)
        except socket.timeout:
            sent = sock.sendto(data, server_address)
            adk, server = sock.recvfrom(bufferSize)

        adk = int.from_bytes(adk,"little")
        if adk == seqNum + 1:
            seqNum+=1
            fileData = file_to_send.read(bufferSize - 5)
            bytesData = seqNum.to_bytes(5,"little")
            data = bytesData + fileData

        else:
            print("adk is: ",adk," seqNum is: ",seqNum + 1 ," they did not match")
            sock.settimeout(0.800)
            sent = sock.sendto(data, server_address)
            try:
                sock.settimeout(0.800)
                adk, server = sock.recvfrom(bufferSize)
                sent = sock.sendto(data, server_address)
                adk, server = sock.recvfrom(bufferSize)
                adk = int.from_bytes(adk,"little")
            except socket.timeout:
                sock.settimeout(0.800)
                sent = sock.sendto(data, server_address)
                adk, server = sock.recvfrom(bufferSize)
                adk = int.from_bytes(adk,"little")
            if adk == seqNum + 1:
                seqNum+=1
                fileData = file_to_send.read(bufferSize - 5)
                bytesData = seqNum.to_bytes(5,"little")
                data = bytesData + fileData

        if data[5:] == b'':
            test = False
            break

    try:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
    except socket.timeout:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
        print("did not send eof")

    try:
        sock.settimeout(0.600)
        adk, server = sock.recvfrom(bufferSize)
    except socket.timeout:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
        adk, server = sock.recvfrom(bufferSize)
    adk = adk[:5]
    adk = int.from_bytes(adk,"little")
    if adk == 'ok':
        print("got adk from server for the ",x,"time")

        print('I am finishing sending file', fileName,' for the ',x,'th  time')
        file_to_send.close()
        #recording the end time
        endTime = datetime.now()
        timeTaken = int((endTime - startTime).total_seconds() * 1000)
        totalTime += timeTaken
        print('The time used in millisecond to send ', fileName ,' for ', x,'th time is: ',timeTaken,"\n")
        sock.close()
elapsed = str(time.time() - s_time)
print('The average time to send file ',fileName,' in millisecond is: ',totalTime/numTimesSend)
print('Total time to send file ',fileName,' for ',numTimesSend,' times in millisecond is: ',totalTime)
print("\nElapsed: " + elapsed)
print('I am done')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (serverAddress, serverPort)
BLOCKSIZE = 65536
hasher = hashlib.sha1()
with open(fileName, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
print(hasher.hexdigest().encode('utf8'))
sock.settimeout(10)
sent = sock.sendto(hasher.hexdigest().encode('utf8'), server)
sock.close
