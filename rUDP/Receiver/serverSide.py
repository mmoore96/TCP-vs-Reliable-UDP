import socket
import filecmp
from datetime import datetime
import time
import sys
from socket import AF_INET, SOCK_DGRAM
import hashlib
#initializing host, port
serverAddress = '000.000.0.00' #PUT the Server IP HERE!
serverPort = 10002 
#starting the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(15);
server_address = (serverAddress, serverPort)
s.bind(server_address)
totalTime = 0
print('I am ready for any client side request \n')

#change depending on how many files you will be receiving
totalFilesCount = 20
i=0;
fileName = 'receive.txt';

timeToStart = 0
bufferSize = 8192
startSeqNum = 30000

while True:
    i = i+1
    file = 'receive'+str(i)+'.txt';

    #opening the file to write
    f = open(file, 'wb')
    startTime = datetime.now()
    start_time = time.time()
    while timeToStart == 0:
            sTime = datetime.now()
            s_time = time.time()
            timeToStart = 1
    data, server = s.recvfrom(bufferSize)
    print('I am starting receiving file ', fileName, 'for the ',i,'th time')
    check = True
    while data:
        fileSeqNum = data[:5]
        seqNum = int.from_bytes(fileSeqNum,"little")
        if startSeqNum == seqNum:
            seqNum+=1
            startSeqNum+=1
            adk = seqNum.to_bytes(5,"little")
            data = data[5:]
            f.write(data)
        else:
            adk = startSeqNum.to_bytes(5,"little")
        try:
            s.settimeout(0.600)
            sent = s.sendto(adk, server)
        except socket.timeout:
            s.settimeout(1)
            sent = s.sendto(adk, server)

        try:
            s.settimeout(2)
            data, server = s.recvfrom(bufferSize)
        except socket.timeout:
            sent = s.sendto(adk, server)
            data, server = s.recvfrom(bufferSize)
        
        eofData = data[5:]
        try:
            if data.decode('utf8') == '-1':
                fileSeqNum = data[:5]
                seqNum = int.from_bytes(fileSeqNum,"little")
                seqNum+=1
                adk = seqNum.to_bytes(5,"little")

                okAdk = 'ok'.encode('utf8')
                toSend = adk + okAdk
                sent = s.sendto(toSend, server)
                f.close
                break
        except UnicodeDecodeError:
            error = "decode error"

    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('I am finishing receiving file ', fileName, 'for the ',i,'th time ')
    
    
    print('The time used in millisecond to receive ', fileName ,' for ', i,'th time is: ',timeTaken,'\n')
    if i == totalFilesCount:   
        break;
    try:
        seqNum+=1
        adk = seqNum.to_bytes(5,"little")
        s.settimeout(0.600)
        sent = s.sendto(adk, server)
    except socket.timeout:
        s.settimeout(1)
        sent = s.sendto(adk, server)
        
elapsed = str(time.time() - s_time)
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/totalFilesCount)
print('Total time to receive file ',fileName,' for ',totalFilesCount,' times in millisecond is: ',totalTime)
print("\nElapsed: " + elapsed)

f=0
#checking whether the correct data is recieved or not
hashFun, server = s.recvfrom(bufferSize)
s.close()
for x in range(totalFilesCount):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    x += 1
    with open('receive'+str(x)+'.txt', 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
        if hashFun.decode('utf8') != hasher.hexdigest():
            f += 1

print(f , ' Times out of ' , totalFilesCount , ' are not correct!')
print('I am done')
