import socket
from datetime import datetime, time
import time
import threading
import filecmp

#initializing host, port, filename, total time and number of times to send the file
serverAddress = "localhost"
serverPort = 10015
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = (serverAddress, serverPort)
fileName = "send.txt"
totalTime = 0
numTimesSend = 100
print('I am connecting to server side: ', serverAddress,'\n')

#using a for loop to send the file 100 times 

for x in range(numTimesSend):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (serverAddress, serverPort)
    fileName = "send.txt"
    #recording the start time
    startTime = datetime.now()
    start_time = time.time()
    #print("Request started at: " + str(datetime.datetime.utcnow()))
    #connecting to the server
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #server_address = (serverAddress, serverPort)
    x+=1
    #s.send('name.txt'.ljust(100).encode('utf-8'))
    print('I am sending file', fileName,' for the ',x,'th  time')
    #opening file to read
    file_to_send = open(fileName, 'rb')    
    #reading the first 1024 bits
    data = file_to_send.read(1024)
    #sock.sendto(data, server_address)
    while data:
        print(x)
        sent = sock.sendto(data, server_address)
        print("sending")
        #reading the next 1024 bits
        data = file_to_send.read(1024)
            
    
    print('I am finishing sending file', fileName,' for the ',x,'th  time')
    file_to_send.close()
    #recording the end time
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('The time used in millisecond to receive ', fileName ,' for ', x,'th time is: ',timeTaken,"\n")
    sock.close()
#sock.close()
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/numTimesSend)
print('Total time to receive file ',fileName,' for ',numTimesSend,' times in millisecond is: ',totalTime)
print("\nElapsed: " + str(time.time() - start_time))
print('I am done')


