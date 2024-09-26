# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
  
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Listening for connections, queue size of 1
  
    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept connection from client
    
        try:
            # Receive the request from the client
            message = connectionSocket.recv(1024).decode()  # Get the client's message and decode it
            filename = message.split()[1]  # Extract the file requested by the client
            
            # Open and read the file requested
            f = open(filename[1:], 'rb')  # Open the file and read it as bytes
            
            # Send response header for a valid request
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html; charset=UTF-8\r\n"
            response_header += "Server: Simple-Python-WebServer\r\n"
            response_header += "\r\n"  # End the headers with a blank line

            connectionSocket.send(response_header.encode())  # Send the headers

            # Send the content of the requested file to the client
            outputdata = f.read()
            connectionSocket.send(outputdata)  # Send file content
            f.close()

            # Close the connection to the client
            connectionSocket.close()
    
        except IOError:
            # Send response for a file not found (404 error)
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "\r\n"
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(response_header.encode())  # Send the headers
            connectionSocket.send(response_body.encode())  # Send the 404 HTML response

            # Close the connection to the client
            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
