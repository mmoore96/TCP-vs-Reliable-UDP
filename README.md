# TCP vs Reliable UDP

Two python programs to test the efficiency of file transfer using TCP vs reliable UDP.

## Installation

You can download the files directly from github or using git clone in terminal.

```bash
git clone https://github.com/mmoore96/TCP-vs-Reliable-UDP.git
```

## Setup
1. Choose either TCP or rUDP and enter the directory.
2. Open the serverSide and clientSide files in an IDE or text editor of your liking.
3. Change the following lines of code and enter the IP Address and port number.

TCP/Receiver/serverSide.py:
```python
#initializing host, port
HOST = '000.000.0.00' #PUT the Server IP HERE!
PORT = 10002 #Change port number to match your router settings
```
TCP/Sender/clientSide.py:
```python
#initializing host, port, filename, total time and number of times to send the file
host = '000.000.0.00' #PUT the Server IP HERE!
port = 10002 #Change port number to match your router settings
```

rUDP/Receiver/serverSide.py:
```python
#initializing host, port
serverAddress = '000.000.0.00' #PUT the Server IP HERE!
serverPort = 10002 #Change port number to match your router settings
```

rUDP/Sender/clientSide.py:
```python
#initializing host, port, filename, total time and number of times to send the file
serverAddress = '000.000.0.00' #PUT the Server IP HERE!
serverPort = 10002 #Change port number to match your router settings
```
## Usage
1. Run the gen.py script inside the Sender directory(both TCP/rUDP) to generate the files to be sent OR use your own file.
```bash
python3 gen.py
```
2. You can copy the contents of the files that were generated by gen.py to the file named send.text OR change the variable "fileName" in clientSide.py(applies to both TCP/rUDP).
```python
#Can be changed to which ever file you want to send.
fileName = "send.txt"
```
3. Once these changes have been made, ensure you save the python file.

4. Run Receiver/serverSide.py FIRST.

```bash
python3 serverSide.py
```

5. Run Sender/clientSide.py SECOND
```bash
python3 serverSide.py
```

## Output

Server Side:
```bash
Receiver % python3 serverSide.py
I am ready for any client side request 

I am starting receiving file  receive.txt for the  1 th time
I am finishing receiving file  receive.txt for the  1 th time 
The time used in millisecond to receive  receive.txt  for  1 th time is:  1244 

I am starting receiving file  receive.txt for the  2 th time
I am finishing receiving file  receive.txt for the  2 th time 
The time used in millisecond to receive  receive.txt  for  2 th time is:  0 

I am starting receiving file  receive.txt for the  3 th time
I am finishing receiving file  receive.txt for the  3 th time 
The time used in millisecond to receive  receive.txt  for  3 th time is:  0 

I am starting receiving file  receive.txt for the  4 th time
I am finishing receiving file  receive.txt for the  4 th time 
The time used in millisecond to receive  receive.txt  for  4 th time is:  0 

I am starting receiving file  receive.txt for the  5 th time
I am finishing receiving file  receive.txt for the  5 th time 
The time used in millisecond to receive  receive.txt  for  5 th time is:  0 

The average time to receive file  receive.txt  in millisecond is:  248.8
Total time to receive file  receive.txt  for  5  times in millisecond is:  1244

Elapsed: 1.247298002243042
0  Times out of  5  are not correct!
I am done
```

Client Side:
```bash
Sender % python3 clientSide.py
I am connecting to server side:  000.000.0.00 

I am sending file send.txt  for the  1 th  time
I am sending file send.txt  for the  2 th  time
I am sending file send.txt  for the  3 th  time
I am sending file send.txt  for the  4 th  time
I am sending file send.txt  for the  5 th  time
The average time to send file  send.txt  in millisecond is:  0.0
Total time to send file  send.txt  for  5  times in millisecond is:  0

Elapsed: 0.0027921199798583984
I am done
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GNU General Public License v3.0
