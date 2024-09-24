import socket

class Server:
    def __init__(self, chunk_size, file_name):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 5050))
        self.server.listen()
        
        self.chunk_size = chunk_size
        self.file_name = file_name
        self.is_send = False
    
    def run(self):
        self.client_socket, _ = self.server.accept()
        while True:
            if not self.file_name or not self.is_send: continue
            file = open(self.file_name, mode="rb")
            data = file.read(self.chunk_size)

            while data:
                self.client_socket.send(data)
                data = file.read(self.chunk_size)
        
            file.close()
            self.file_name = None
            self.is_send = False
        
    
    def close_server(self):
        self.server.close()
