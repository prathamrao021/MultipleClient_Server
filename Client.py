import socket
import os
import sys 

def send_file_content(server_socket, filename):
    """
    Sends the content of a file to the server.

    Args:
        server_socket (socket.socket): The server socket.
        filename (str): The name of the file to send.
    """
    with open(filename, 'rb') as file:
        chunk = file.read(1024)
        while chunk:
            server_socket.send(chunk)
            chunk = file.read(1024)
    server_socket.send(b'END_OF_FILE')  

def receive_file_content(server_socket, filename):
    """
    Receives the content of a file from the server.

    Args:
        server_socket (socket.socket): The server socket.
        filename (str): The name of the file to receive.
    """
    with open(filename, 'wb') as file:
        while True:
            chunk = server_socket.recv(1024)
            if chunk.endswith(b'END_OF_FILE'):
                chunk = chunk[:-len(b'END_OF_FILE')]
                file.write(chunk)
                break
            file.write(chunk)

def client(port):
    """
    Starts the client and handles the communication with the server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', int(port)))

        while True:
            command = input("Enter command: ")
            client_socket.send(command.encode())

            if command == 'exit':
                client_socket.send('exit'.encode())
                break
            elif command.startswith('get'):
                _, filename = command.split()
                response = client_socket.recv(5).decode()  
                if response == 'BEGIN':
                    receive_file_content(client_socket, 'new' + filename)
                    print("File received.")
                else:
                    print("File not found on server.")
            elif command.startswith('upload'):
                _, filename = command.split()
                if os.path.isfile(filename):
                    send_file_content(client_socket, filename)
                    print("File sent.")
                else:
                    print("File doesn't exist on the client.")
            else:
                print("Note: get, upload and exit are the only valid commands.")

if __name__ == '__main__':
    # port = sys.argv[1]
    client(port=5160)