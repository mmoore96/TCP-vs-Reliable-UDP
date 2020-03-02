import socket
import filecmp
from datetime import datetime
import sys
from socket import AF_INET, SOCK_DGRAM
#initializing host, port
serverAddress = "localhost"
serverPort = 10015
#starting the server

while True:
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #recording the start time
    #s.bind(server_address)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(30);
    server_address = (serverAddress, serverPort)
    #s.bind(server_address)
    totalTime = 0
    print('I am ready for any client side request \n')
    totalFilesCount = 2
    i=0;
    fileName = 'receive.txt';
    #userInput = input("\nRequested file: ")
    #message = 'y'.encode();
    print('Requesting %s' % fileName)
    #sent = s.sendto(message, server_address)
    adk = "ok"
    startTime = datetime.now()
    i = i+1
    print(i)
    file = 'receive'+str(i)+'.txt';
    print('I am starting receiving file ', fileName, 'for the ',i,'th time')
    #opening the file to write
    #data, server = s.recvfrom(1024)
    f = open(file, 'w')
    data, server = s.recvfrom(1024)
    #data = data
    print(data)
    try:
        while (data):
            f.write(data)
            s.settimeout(2)
            data, server = s.recvfrom(1024)
            s.sendto(adk, server_address) 
            print("Hello")
        
        f.close()
        
    except:
        f.close()
        sent = s.sendto(message, server_address)
        print('I am finishing receiving file ', fileName, 'for the ',i,'th time ')
        #recording the end time
        endTime = datetime.now()
        timeTaken = int((endTime - startTime).total_seconds() * 1000)
        totalTime += timeTaken
        print('The time used in millisecond to receive ', fileName ,' for ', i,'th time is: ',timeTaken,'\n')
        if i == totalFilesCount: break;
        #s.close()
s.close()
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/totalFilesCount)
print('Total time to receive file ',fileName,' for ',totalFilesCount,' times in millisecond is: ',totalTime)
f=0
#checking whether the correct data is recieved or not

##TODO: has this bad boy!!

for x in range(totalFilesCount):
    x += 1
    res = filecmp.cmp('receive.txt','receive'+str(x)+'.txt',shallow=False)
    if res == False: f += 1
print(f , ' Times out of ' , totalFilesCount , ' are not correct!')
print('I am done')



    



