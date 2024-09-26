# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    # Create a TCP socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    serverSocket = socket(AF_INET, SOCK_STREAM)
  
    # Bind the server socket to the given port on all available network interfaces
    serverSocket.bind(("", port))
    # Start listening for incoming connections, with a queue size of 1 (one connection at a time)
    serverSocket.listen(1)
  
    while True:
        # When the server is prepared to accept connections, display a message.
        print('Ready to serve...')
        # Accept a client's connection. This stops in the event that a connection is made.
        connectionSocket, addr = serverSocket.accept()  # 'addr' holds the client's address
        try:
            # After receiving the client's request, decode it into string format.
            try:
                # Try to receive the data and decode it
                message = connectionSocket.recv(1024)
                if message:
                    message = message.decode()
                else:
                    message = ""
            except UnicodeDecodeError:
                # Handle decoding errors gracefully
                message = ""
            # Extract the filename from the second element of the request line by splitting the HTTP request message.
            try:
              request_parts = message.split()
              filename = request_parts[1] if len(request_parts) > 1 else "/"
            except IndexError:
              filename = "/"
            # Ignore the first '/' in the file path and open the required file from the disk in binary read mode ('rb').
            f = open(filename[1:], 'rb')
            # Read the entire file content
            outputdata = f.read()
            # Close the file after reading
            f.close()
            
            # Create the HTTP response header (200 OK) in the event that a file retrieval is successful.
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html; charset=UTF-8\r\n"  # Specify content type and character encoding
            response_header += "Server: Simple-Python-WebServer\r\n"  # Indicate the server's name
            response_header += "Connection: close\r\n"  # Close the connection after sending the response
            response_header += "\r\n"  # Blank line to separate headers from body

            # Combine the response header and the file content (body) into one message
            response = response_header.encode() + outputdata
            # Send the response back to the client
            connectionSocket.send(response)

            # Close the connection to the client after sending the response
            connectionSocket.close()
    
        except IOError:
            # Handle cases where the requested file is not found by sending a 404 Not Found error
            
            # Construct the HTTP response header for a 404 error
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += "Content-Type: text/html\r\n"  # Indicate that the response is HTML
            response_header += "Connection: close\r\n"  # Close the connection after the response
            response_header += "\r\n"  # End of the headers
            
            # Construct a simple HTML body to display a '404 Not Found' message to the user
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"
            # Combine the header and body into one message
            response = response_header.encode() + response_body.encode()

            # Send the 404 error response to the client
            connectionSocket.send(response)

            # Close the connection to the client after sending the error response
            connectionSocket.close()

# If you are running this script directly without importing it, launch the web server on the specified port.
if __name__ == "__main__":
    webServer(13331)  # Start the server on port 13331