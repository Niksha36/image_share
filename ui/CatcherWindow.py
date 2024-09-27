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


        # Через 5 сек устанавливается дефолтное изображение
        # self.root.after(5000, self.set_default_image)

    def create_catcher_window(self):
        self.app.clear_window()
        tk.Label(self.root, text="Catcher Mode", font=("Arial", 20)).pack(pady=20)

        self.app.image_label = tk.Label(
            self.root,
            highlightbackground="#339AF0",  # Border color
            highlightcolor="#339AF0",  # Border color when focused
            highlightthickness=3,  # Border thickness
            relief="solid",  # Border style
            text="The image sent by the sender will be here",
            font=("Arial", 12),
        )
        self.app.image_label.place(x=40, y=85, relwidth=1, relheight=1, anchor="nw", width=-80, height=-120)

        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=10)

    # предпросмотр того как работает сейчас показ картинок
    # def set_default_image(self):
    #     default_image_path = r"C:\Users\Nikita\PycharmProjects\image_share\app_icon.png"
    #     self.display_image(default_image_path)

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
            label_width = self.app.image_label.winfo_width()
            label_height = self.app.image_label.winfo_height()

            # Calculate the aspect ratio
            img_ratio = img.width / img.height
            label_ratio = label_width / label_height

            if img_ratio > label_ratio:
                # Image is wider than the label
                new_width = label_width
                new_height = int(label_width / img_ratio)
            else:
                # Image is taller than the label
                new_height = label_height
                new_width = int(label_height * img_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.app.image_label.config(
                image=img,
                text="",
                width=new_width,
                height=new_height,
                highlightthickness=0,  # Remove border
                relief="flat"  # Remove border style
            )
            self.app.image_label.image = img
        except Exception as e:
            print(e)
            messagebox.showwarning("Error reading file", "The sender sent an invalid file.")
