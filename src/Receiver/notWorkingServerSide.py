import socket
import filecmp
from datetime import datetime
import sys
from socket import AF_INET, SOCK_DGRAM
#initializing host, port
serverAddress = "localhost"
serverPort = 10031
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
while True:
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #recording the start time
    #s.bind(server_address)
    startTime = datetime.now()
    i = i+1
    print(i)
    file = 'receive'+str(i)+'.txt';
    
    print('I am starting receiving file ', fileName, 'for the ',i,'th time')
    #opening the file to write
    #data, server = s.recvfrom(1024)
    f = open(file, 'wb')
    data, server = s.recvfrom(1024)
    #data = data
    #print(data)
    check = True
    while check:
        f.write(data)
        #s.settimeout(15)
        try:
            s.settimeout(15)
            sent = s.sendto(adk, server_address)
        except:
            print("did not send adk")
            check = False  
        data, server = s.recvfrom(1024)
        print(data)
        if data == b'-1':
            f.close
            break
        
        #f.close()
    #f.close()
    print('I am finishing receiving file ', fileName, 'for the ',i,'th time ')
    #recording the end time
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    print('The time used in millisecond to receive ', fileName ,' for ', i,'th time is: ',timeTaken,'\n')
    if i == totalFilesCount:   
        break;
    try:
        sent = s.sendto(adk, server_address)
    except:
        print("did not send adk") 
    #s.close()
s.close()
print('The average time to receive file ',fileName,' in millisecond is: ',totalTime/totalFilesCount)
print('Total time to receive file ',fileName,' for ',totalFilesCount,' times in millisecond is: ',totalTime)
f=0
#checking whether the correct data is recieved or not
for x in range(totalFilesCount):
    x += 1
    res = filecmp.cmp('receive.txt','receive'+str(x)+'.txt',shallow=False)
    if res == False: f += 1
print(f , ' Times out of ' , totalFilesCount , ' are not correct!')
print('I am done')

    



