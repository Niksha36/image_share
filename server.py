import socket
import threading



class Server:
    def __init__(self, chunk_size, file_name, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen()
        self.server.settimeout(2)
        self.is_close = False
        
        self.chunk_size = chunk_size
        self.file_name = file_name

    def run(self, client_socket):
        while not self.is_close:
            if not self.file_name: continue

            file = open(self.file_name, mode="rb")
            data = file.read(self.chunk_size)

            while data:
                client_socket.send(data)
                data = file.read(self.chunk_size)
        
            file.close()
            self.file_name = None

    def accept_clients(self):
        while not self.is_close:
            try:
                client_socket, _ = self.server.accept()
                threading.Thread(target=self.run, args=(client_socket,), daemon=True).start()
            except socket.timeout:
                pass
            except OSError:
                if self.is_close:
                    break

    def close_server(self):
        print("SERVER CLOSE")
        self.server.close()
        self.is_close = True
