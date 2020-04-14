import socket
import filecmp
from datetime import datetime
import hashlib
import time
#initializing host, port
HOST = '192.168.1.34'
PORT = 10004
#starting the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
totalTime = 0
print('I am ready for any client side request \n')
totalFilesCount = 3
bufferSize = 8192
i=0;
timeToStart = 0
fileName = 'rec.txt';
while True:
    conn, addr = s.accept()
    #recording the start time
    startTime = datetime.now()
    i = i+1
    
    file = 'receive'+str(i)+'.txt';
    
    print('I am starting receiving file ', fileName, 'for the ',i,'th time')
    #opening the file to write
    f = open(file, 'wb')
    while timeToStart == 0:
            sTime = datetime.now()
            s_time = time.time()
            timeToStart = 1
    data = conn.recv(bufferSize)
    while (data):
        f.write(data)
        data = conn.recv(bufferSize)
    
    f.close()

    print('I am finishing receiving file ', fileName, 'for the ',i,'th time ')
    #recording the end time
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('The time used in millisecond to receive ', fileName ,' for ', i,'th time is: ',timeTaken,'\n')
    if i == totalFilesCount: break;
    conn.close()
#s.close()
elapsed = str(time.time() - s_time)
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/totalFilesCount)
print('Total time to receive file ',fileName,' for ',totalFilesCount,' times in millisecond is: ',totalTime)
print("\nElapsed: " + elapsed)
f=0
conn, addr = s.accept()
hashFun = conn.recv(bufferSize)

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
conn.close()    
s.close()
