import os.path
import socket 
import select

class Client:
    def __init__(self, chunk_size, file_name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(4)
        
        self.chunk_size = chunk_size
        self.file_name = file_name
        self.is_download = False
        self.client_closed = False
        self.counts_download = 0
    
    def run(self) -> None:
        ready = select.select([self.client], [], [], 1)
        if ready[0] and self.client.fileno() != -1: 
            self.image_path = f"{self.file_name}_{self.counts_download}"
            while os.path.exists(self.image_path + ".jpg"): self.image_path += "_0"
            self.image_path += ".jpg"
            
            file = open(self.image_path, mode="wb")
            while ready[0]:
                data = self.client.recv(self.chunk_size)
                file.write(data)
                ready = select.select([self.client], [], [], 1)
            
            file.close()
            self.counts_download += 1
            self.is_download = True
        
    def close_client(self) -> None:
        print("CLIENT CLOSE")
        self.client.close()
        self.client_closed = True
