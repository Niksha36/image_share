import threading
import tkinter as tk
import socket
from tkinter import messagebox

from PIL import ImageTk, Image

from client import Client


class CatcherWindow:
    def __init__(self, root, app, server_ip, port):
        self.root = root
        self.app = app
        
        self.server_ip = server_ip
        self.port = port
        threading.Thread(target=self.receive_file, daemon=True).start()
        
        self.create_catcher_window()

    def create_catcher_window(self):
        self.app.clear_window()
        tk.Label(self.root, text="Catcher Mode", font=("Arial", 20)).pack(pady=20)
        self.app.image_label = tk.Label(self.root, text="The image sent by the sender will be here", font=("Arial", 12), width=40, height=10, relief="solid")
        self.app.image_label.pack(pady=10)
        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=10)

    def receive_file(self):
        client = Client(self.app.chunk_size, self.app.client_name_files)
        try:
            client.client.connect((self.server_ip, self.port))
            print("CLIENT CONNECTED")
        except socket.error as e:
            messagebox.showwarning("Connection error", "Failed to connect to the server. Please try again later.")
            self.app.go_back()
            return

        while True:
            try:
                client.run()
            except:
                messagebox.showwarning("Connection to the server was lost.", "Reconnect to the server.")
                self.app.go_back()
                return

            if client.is_download:
                self.display_image(f"{self.app.client_name_files}_{self.app.count_images}.jpg")
                self.app.count_images += 1
                client.is_download = False
            if client.client_closed:
                break

    def display_image(self, image_path):
        try:
            img = Image.open(image_path) 
            img = ImageTk.PhotoImage(img)
            self.app.image_label.config(image=img, text="", width=img.width(), height=img.height())
            self.app.image_label.image = img
        except:
            messagebox.showwarning("Error reading file", "The sender sent an invalid file.")
