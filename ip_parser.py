from threading import Thread, Lock
from time import perf_counter
from sys import stderr
from time import sleep
import socket



class Threads:
    def __init__(self, threads: int =30):
        self.thread_lock = Lock()
        self.functions_lock = Lock()
        self.functions = []
        self.threads = []
        self.nthreads = threads
        self.running = True
        self.print_lock = Lock()

    def stop(self) -> None:
        self.running = False

    def append(self, function, *args) -> None:
        self.functions.append((function, args))

    def start(self) -> None:
        for i in range(self.nthreads):
            thread = Thread(target=self.worker, daemon=True)
            thread._args = (thread, )
            self.threads.append(thread)
            thread.start()

    def join(self) -> None:
        for thread in self.threads:
            thread.join()

    def worker(self, thread:Thread) -> None:
        while self.running and (len(self.functions) > 0):
            with self.functions_lock:
                function, args = self.functions.pop(0)
            function(*args)

        with self.thread_lock:
            self.threads.remove(thread)


class Parser:
    def __init__(self, verbose=False):
        self.all_ip = [] 
        self.verbose = verbose

    def parse(self, base_ip, port):
        self.all_ip = []
        self.start = perf_counter()
        socket.setdefaulttimeout(0.1)

        self.threader = Threads(30)
        if "." in base_ip:
            for i in range(1, 256):
                self.threader.append(self.connect, base_ip + f".{i}", port)
        else:
            self.threader.append(self.connect, base_ip, port)
        self.threader.start()
        self.threader.join()

    def connect(self, ip_address, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex((ip_address, port))
        with self.threader.print_lock:
            if result != 0: return
            self.all_ip.append(ip_address)
            if self.verbose:
                stderr.write(f"[{perf_counter() - self.start:.5f}] Found {ip_address} HostName {self.getHost(ip_address)} Port {port}\n")
    
    def getHost(self, ip_addres):
        try: 
            return socket.gethostbyaddr(ip_addres)
        except: 
            return ""


if __name__ == "__main__":
    parser = Parser(verbose=True)

    client_ip = socket.gethostbyname(socket.gethostname())
    print("IP ADRESS:", client_ip)
    parser.parse(".".join(client_ip.split(".")[:2]) + ".144", 5050)
