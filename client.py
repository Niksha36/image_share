import socket 
import select

class Client:
    def __init__(self, chunk_size, file_name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.chunk_size = chunk_size
        self.file_name = file_name
        self.is_download = False
        self.client_closed = False
        self.counts_download = 0
    
    def run(self):
        ready = select.select([self.client], [], [], 1)
        if ready[0]: 
            file = open(f"{self.file_name}_{self.counts_download}.jpg", mode="wb")
            while ready[0]:
                data = self.client.recv(self.chunk_size)
                file.write(data)
                ready = select.select([self.client], [], [], 1)
            
            file.close()
            self.counts_download += 1
            self.is_download = True
        
    def close_client(self):
        print("CLIENT CLOSE")
        self.client.close()
        self.client_closed = True
