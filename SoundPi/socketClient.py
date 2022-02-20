"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""
import time
import socket
import base64

hostMACAddress = 'E4:5F:01:6A:57:BD' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 1 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
#while 1:
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    #    data = client.recv(size)

    #str = b'[[100, 100]]!'
    str = b'[[512, 226], [423, 432]]!'
    
    #str = b'[[121, 246], [30, 40]]!'
    
    str = b'[[1512, 1226], [1423, 432], [734, 2234]]!'
    #str = b'[[823, 2012], [1012, 1226], [1423, 1432], [1234, 1234], [1351, 1128], [1231, 1283]]!'
    client.send(str)
    print(str)

    client.close()
    s.close()

#while True:
 # str = b'[[512, 226], [423, 432], [234, 234], [351,128], [231, 983]]!'
  #client.send(str)
  #print(str)

#client.close()

#      data = b"hi"
#     while True:
#       client.send(data)
#      time.sleep(1)
# print(data)
except:	
    print("Closing socket")	
    client.close()
    s.close()
    exit(1)


#sb = b''
#fh = open("image.jpeg", "wb")

#while 1:
#    data = client.recv(size)
#    if data:
#        print(data)

 #       if data[len(data)-3::] == b'EOF':
 #           fh.write(base64.b64decode(sb))
  #          fh.close()
   #         print("Image Received, closing socket")	
    #        client.close()
     #       s.close()
      #      exit(0)
            #break

       # sb += data
#client.send(data)
#while 1:
