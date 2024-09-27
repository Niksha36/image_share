import socket
import threading
import time

class Server:
    def __init__(self, chunk_size, file_name, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen()

        self.is_close = False
        self.chunk_size = chunk_size
        self.file_name = file_name

    def run(self, client_socket) -> None:
        while not self.is_close:
            try:
                if not self.file_name: continue
                with open(self.file_name, mode="rb") as file:
                    client_socket.sendall(file.read())
                    self.file_name = None
            except:  # When the client disconnects, the server closes the stream
                break

    def accept_clients(self) -> None:
        while not self.is_close:
            try:
                client_socket, _ = self.server.accept()    
                
                if client_socket.recv(9) != b"ITCLIENT": continue  # In order to avoid creating a thread for parsers etc.
                threading.Thread(target=self.run, args=(client_socket,), daemon=True).start()
            except:
                pass

    def close_server(self) -> None:
        print("SERVER CLOSE")
        self.server.close()
        self.is_close = True
