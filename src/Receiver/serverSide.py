import socket
import filecmp
from datetime import datetime
import time
import sys
from socket import AF_INET, SOCK_DGRAM
import hashlib
#initializing host, port
serverAddress = "localhost"
serverPort = 10032
#starting the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(15);
server_address = (serverAddress, serverPort)
s.bind(server_address)
totalTime = 0
print('I am ready for any client side request \n')
totalFilesCount = 5
i=0;
fileName = 'receive.txt';
adk = 'ok'.encode('utf8')
timeToStart = 0
bufferSize = 8192
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
        f.write(data)
        #s.settimeout(15)
        try:
            s.settimeout(15)
            sent = s.sendto(adk, server)
        except:
            print("did not send adk")
            #check = False  
        data, server = s.recvfrom(bufferSize)
        #print(data)
        if data.decode('utf8') == '-1':
            sent = s.sendto(adk, server)
            f.close
            break
        
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
        sent = s.sendto(adk, server)
    except:
        print("did not send adk") 
    #s.close()
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
    #print(hasher.hexdigest())
    #res = filecmp.cmp('receive.txt','receive'+str(x)+'.txt',shallow=False)
    if hashFun.decode('utf8') != hasher.hexdigest():
        f += 1
    #if res == False: f += 1
print(f , ' Times out of ' , totalFilesCount , ' are not correct!')
print('I am done')
