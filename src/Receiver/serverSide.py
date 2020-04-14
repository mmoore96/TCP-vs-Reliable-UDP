import socket
import filecmp
from datetime import datetime
import time
import sys
from socket import AF_INET, SOCK_DGRAM
import hashlib
#initializing host, port
serverAddress = '192.168.1.104' #'192.168.1.34'
serverPort = 10002 #33822
#starting the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(15);
server_address = (serverAddress, serverPort)
s.bind(server_address)
totalTime = 0
print('I am ready for any client side request \n')
totalFilesCount = 10
i=0;
fileName = 'receive.txt';
#adk = 'ok'.encode('utf8')
timeToStart = 0
bufferSize = 8192
startSeqNum = 30000

while True:
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #recording the start time
    #s.bind(server_address)
    i = i+1
    #print(i)
    file = 'receive'+str(i)+'.txt';

    #opening the file to write
    #data, server = s.recvfrom(1024)
    f = open(file, 'wb')
    startTime = datetime.now()
    start_time = time.time()
    while timeToStart == 0:
            sTime = datetime.now()
            s_time = time.time()
            timeToStart = 1
    data, server = s.recvfrom(bufferSize)
    print('I am starting receiving file ', fileName, 'for the ',i,'th time')
    #data = data
    #print(data)
    check = True
    while data:
        fileSeqNum = data[:5]
        seqNum = int.from_bytes(fileSeqNum,"little")
        print (seqNum)
        if startSeqNum == seqNum:
            seqNum+=1
            startSeqNum+=1
            adk = seqNum.to_bytes(5,"little")
            data = data[5:]
            f.write(data)
        else:
            adk = startSeqNum.to_bytes(5,"little")
            #sent = s.sendto(adk, server)    
        #s.settimeout(15)
        try:
            s.settimeout(0.600)
            sent = s.sendto(adk, server)
            print("sent adk for the ",i,"th time")
        except socket.timeout:
            print("did not send adk")
            s.settimeout(1)
            sent = s.sendto(adk, server)
            #check = False  

        try:
            s.settimeout(0.800)
            data, server = s.recvfrom(bufferSize)
            # fileSeqNum = data[:5]
            # newSeqNum = int.from_bytes(fileSeqNum,"little")
            # if newSeqNum != seqNum:
            #     sent = s.sendto(adk, server)
            #     data, server = s.recvfrom(bufferSize)
            #     seqNum+=1
            #     adk = seqNum.to_bytes(5,"little")
            #     sent = s.sendto(adk, server)
            #     f.write(data)
            # else:
            #     break
                    
        except socket.timeout:
            s.settimeout(0.800)
            sent = s.sendto(adk, server)
            data, server = s.recvfrom(bufferSize)
            #check = False      
        #data, server = s.recvfrom(bufferSize)
        #print(data)
        
        eofData = data[5:]
        #print(data)
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
            print("decode error")    
        
        #f.close()
    #f.close()
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('I am finishing receiving file ', fileName, 'for the ',i,'th time ')
    #recording the end time
    
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
        #print("did not send adk") 
    #s.close()
elapsed = str(time.time() - s_time)
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/totalFilesCount)
print('Total time to receive file ',fileName,' for ',totalFilesCount,' times in millisecond is: ',totalTime)
print("\nElapsed: " + elapsed)

f=0
#checking whether the correct data is recieved or not
hashFun, server = s.recvfrom(bufferSize)
#print(hashFun)
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
    #print(hasher.hexdigest())
        #res = filecmp.cmp('receive.txt','receive'+str(x)+'.txt',shallow=False)
        if hashFun.decode('utf8') != hasher.hexdigest():
            f += 1
        #if res == False: f += 1
print(f , ' Times out of ' , totalFilesCount , ' are not correct!')
print('I am done')
   
