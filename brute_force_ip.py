from sys import stderr
from json import detect_encoding
from threading import Thread, Lock
from time import perf_counter

import socket
import select
import psutil
import ipaddress


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
            try:
                thread.join()
            except:
                continue

    def worker(self, thread: Thread) -> None:
        while self.running and (len(self.functions) > 0):
            with self.functions_lock:
                function, args = self.functions.pop(0)
            function(*args)

        with self.thread_lock:
            self.threads.remove(thread)


class BruteForceIp:
    def __init__(self, verbose=False):
        self.ip_adresses = None
        self.verbose = verbose

    def search(self, client_ip: str, port: int) -> None:
        self.ip_adresses = {}

        self.start = perf_counter()
        self.threader = Threads(30)
        for ip in self.get_mask(client_ip):
            self.threader.append(self.connect, ip, port)

        self.threader.start()
        self.threader.join()

    def connect(self, ip_address: str, port: int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            result = sock.connect_ex((ip_address, port))

            with self.threader.print_lock:
                if result != 0: return
                                 
                sock.send(b"ITSEARCH")
                
                try:
                    ready = select.select([sock], [], [], 0.4)
                    if not ready[0]:
                        raise Exception("The server does not say its name.")
                    
                    self.ip_adresses[ip_address] =  sock.recv(32).decode()
                except Exception as e:
                    # print(e)
                    self.ip_adresses[ip_address] = ip_address
    
                if self.verbose:
                    stderr.write(f"[{perf_counter() - self.start:.5f}] Found {ip_address}\n")

    def get_mask(self, client_ip: str) -> list[str]:
        try:
            for net in psutil.net_if_addrs()["Беспроводная сеть"]:
                if net[1] == client_ip:
                    mask = net[2]
                    break

            network = ipaddress.IPv4Network(f"{client_ip}/{mask}", strict=False)
            return list(map(str, ipaddress.IPv4Network(f"{network.network_address}/{mask}")))     
        except: 
            return [client_ip[:client_ip.rfind(".")] + f".{i}" for i in range(256)]
    

if __name__ == "__main__":
    searcher = BruteForceIp(verbose=False)

    client_ip = socket.gethostbyname(socket.gethostname())
    print("IP ADRESS:", client_ip)
    searcher.search(client_ip, 80)
    print(searcher.ip_adresses)
