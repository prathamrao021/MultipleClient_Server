import socket
import sys
import threading
import os

def handle_client(server_socket,client_socket,client_address):
    print(f"Connection established with {client_address}")
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break 
            if command == 'exit':
                break
            elif command.startswith('get'):
                _, filename = command.split()
                if os.path.isfile(filename):
                    client_socket.send('BEGIN'.encode())
                    send_file_content(client_socket, filename)
                    print("File sent successfully.")
                else:
                    client_socket.send(b'File not found')
            elif command.startswith('upload'):
                _, filename = command.split()
                receive_file_content(client_socket, 'new' + filename)
                print("File received successfully.")
    finally:
        server_socket.close()
        client_socket.close()
        print(f"Connection closed with {client_address}")

def send_file_content(client_socket, filename):
    with open(filename, 'rb') as file:
        chunk = file.read(1024)
        while chunk:
            client_socket.send(chunk)
            chunk = file.read(1024)
    client_socket.send(b'END_OF_FILE')

def receive_file_content(client_socket, filename):
        with open(filename, 'wb') as file:
            while True:
                chunk = client_socket.recv(1024)
                if chunk.endswith(b'END_OF_FILE'):
                    chunk = chunk[:-len(b'END_OF_FILE')]
                    file.write(chunk)
                    break
                file.write(chunk)
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5160))
        print("Server is running on port "+str(5160))
        
        while True:
            server_socket.listen(1) 
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(server_socket,client_socket,client_address))
            client_thread.start()
            
            

if __name__ == "__main__":
    server()