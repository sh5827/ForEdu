#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    host = gethostname()            # finding the host name
    serverSocket.bind((host, port)) # Binding host and port
    print(host,port)
    serverSocket.listen(1)          # max 1 connection

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  
        try:
            message = connectionSocket.recv(1024).decode() # 1024 bytes at a time
            filename = message.split()[1]   
            f = open(filename[1:])
            outputdata = f.read()                          # reading the file
            #Send one HTTP header line into socket
            #Fill in start
            connectionSocket.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode()) # adding 200 ok status
            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            #Send response message for file not found (404) 
            connectionSocket.send('HTTP/1.0 404 NOT FOUND\r\n\r\n'.encode()) # adding 404 NOT FOUND status
            connectionSocket.send('404 Not Found'.encode())           
            
            #Close client socket
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
