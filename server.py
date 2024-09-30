import os
import socket
import threading
import time

class Server:
    def __init__(self, file_name: str, port: int):
        print("START SERVER")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen()

        self.file_name = file_name

    def run(self, client_socket: socket.socket) -> None:
        while self.server.fileno() != -1:
            try:
                if not self.file_name:
                    continue
                print(f"Sending file: {self.file_name}")
                file_extension = os.path.splitext(self.file_name)[1]
                file_name = os.path.basename(self.file_name)
                client_socket.sendall(f"{file_name}\n{file_extension}\n".encode())
                with open(self.file_name, mode="rb") as file:
                    client_socket.sendall(file.read())
                self.file_name = None
            except Exception as e:
                print(f"Exception occurred: {e}")
                break

    def accept_clients(self) -> None:
        while self.server.fileno() != -1:
            try:
                client_socket, _ = self.server.accept()
                if client_socket.recv(9) != b"ITCLIENT":
                    continue
                print("Client connected")
                threading.Thread(target=self.run, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print(f"Exception in accept_clients: {e}")

    def close_server(self) -> None:
        print("SERVER CLOSE")
        self.server.close()
