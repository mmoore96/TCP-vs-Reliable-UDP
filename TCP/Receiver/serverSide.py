import socket
from datetime import datetime, time
import time
import hashlib
#initializing host, port, filename, total time and number of times to send the file
host = '24.214.242.190'
port = 10004
fileName = "send.txt"
totalTime = 0
numTimesSend = 100
bufferSize = 8192
print('I am connecting to server side: ', host,'\n')
#using a for loop to send the file 100 times 
for x in range(numTimesSend):
    #recording the start time
    #print("Request started at: " + str(datetime.datetime.utcnow()))
    #connecting to the server
    s = socket.socket()
    ##some -1 ?? check is created or not
    s.connect((host, port))
        
    #s.send('name.txt'.ljust(100).encode('utf-8'))
    print('I am sending file', fileName,' for the ',x,'th  time')
    #opening file to read
    file_to_send = open(fileName, 'rb')    
    #reading the first 1024 bits
    startTime = datetime.now()
    start_time = time.time()
    data = file_to_send.read(bufferSize)
    
    while data:
        s.send(data)
        #reading the next 1024 bits
        data = file_to_send.read(bufferSize)
    print('I am finishing sending file', fileName,' for the ',x,'th  time')
    file_to_send.close()
    #recording the end time
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('The time used in millisecond to receive ', fileName ,' for ', x,'th time is: ',timeTaken,"\n")
    s.close()

print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/numTimesSend)
print('Total time to receive file ',fileName,' for ',numTimesSend,' times in millisecond is: ',totalTime)
print("\nElapsed: " + str(time.time() - start_time))
print('I am done')
s = socket.socket()
s.connect((host, port))
BLOCKSIZE = 65536
hasher = hashlib.sha1()
with open(fileName, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)      
s.send(hasher.hexdigest().encode('utf8'))
s.close()        
