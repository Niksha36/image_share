import socket
import threading
import time
import os

class Server:
    def __init__(self, port: int, server_name: str):
        print("START SERVER")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen()
        self.server_name = server_name

        self.file_path = None

    def run(self, client_socket: socket.socket) -> None:
        while self.server.fileno() != -1:
            try:
                if not self.file_path: continue
                
                file_path, file_extension = os.path.splitext(self.file_path)
                client_socket.sendall(f"{file_path.split("/")[-1]}\n{file_extension}\n".encode())
                time.sleep(0.5)
                print(file_path, file_extension)
                with open(self.file_path, mode="rb") as file:
                    client_socket.sendall(file.read())

                self.file_path = None
            except Exception as e:  # When the client disconnects, the server closes the stream
                print(e)
                break

    def accept_clients(self) -> None:
        while self.server.fileno() != -1:
            try:
                client_socket, _ = self.server.accept()    

                if client_socket.recv(9) != b"ITCLIENT": 
                    client_socket.send(bytes(self.server_name, encoding="utf-8"))
                    continue  # In order to avoid creating a thread for parsers etc.

                threading.Thread(target=self.run, args=(client_socket,), daemon=True).start()
            except:
                pass

    def close_server(self) -> None:
        print("SERVER CLOSE")
        self.server.close()
