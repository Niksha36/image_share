import os.path
import socket 
import select

class Client:
    def __init__(self, chunk_size: int):
        print("CLIENT START")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(4)
        
        self.chunk_size = chunk_size
        self.is_download = False
        self.file_path = None

    def run(self) -> None:
        ready = select.select([self.client], [], [], 1)
        if ready[0] and self.client.fileno() != -1: 
            file_name = self.client.recv(1024).decode().strip().split('\n')
            if len(file_name) < 2: raise Exception("Invalid file name or extension received")
            
            file_name, file_extension = file_name
            self.file_path = os.path.join("./received_images", file_name)
            while os.path.exists(self.file_path + file_extension):
                self.file_path += "(1)"
            self.file_path += file_extension
            
            file = open(self.file_path, mode="wb")
            while ready[0]:
                data = self.client.recv(self.chunk_size)
                if not data: raise
                file.write(data)
                ready = select.select([self.client], [], [], 1)

            file.close()
            self.is_download = True
        
    def close_client(self) -> None:
        print("CLIENT CLOSE")
        self.client.close()
