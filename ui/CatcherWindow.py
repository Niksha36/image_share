import threading
import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk, Image

from client import Client


class CatcherWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
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

        is_connected = False
        # TODO: Add loading icon (spinning circle) while client is not connected to the server
        while not is_connected:
            try:
                client.client.connect(("localhost", 5050))
                is_connected = True
                print("CLIENT CONNECTED")
            except:
                pass

        while True:
            client.run()
            if client.is_download:
                self.display_image(f"{self.app.client_name_files}_{self.app.count_images}.jpg")
                self.app.count_images += 1
                client.is_download = False
            if client.client_closed:
                break

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)  # Corrected this line
            img = ImageTk.PhotoImage(img)
            self.app.image_label.config(image=img, text="", width=img.width(), height=img.height())
            self.app.image_label.image = img
        except:
            messagebox.showwarning("Error reading file", "The sender sent an invalid file.")