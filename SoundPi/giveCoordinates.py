import sys
import socket
import base64

hostMACAddress = 'E4:5F:01:6A:57:BD' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 1 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()

    coordinates = sys.argv[1]
    #print(coordinates)

#    print(1)
    b = bytes(coordinates, 'ascii')
    #b = bytes(coordinates, 'utf-8')
    client.send(b)
    # print(str)
 #   print(2)

    client.close()
    s.close()

except:	
    print("Closing socket")	
    client.close()
    s.close()
    exit(1)
