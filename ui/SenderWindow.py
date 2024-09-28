import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

from server import Server
from ui.utils.rounded_button import create_rounded_rectangle_image


class SenderWindow:
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        
        self.app.server = Server(self.app.chunk_size, self.app.image_path, self.app.port)
        threading.Thread(target=self.app.server.accept_clients, daemon=True).start()
        self.create_sender_window()

    def create_sender_window(self) -> None:
        self.app.clear_window()
        tk.Label(self.root, text="Sender Mode", font=("Arial", 20)).pack(pady=20)
        rounded_select_file_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Select File", "#FFFFFF", self.app.font)
        select_file_button = tk.Button(self.root, image=rounded_select_file_button_image, command=self.select_file, bd=0)
        select_file_button.image = rounded_select_file_button_image
        select_file_button.pack(pady=10)
        rounded_send_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Send", "#FFFFFF", self.app.font)
        send_button = tk.Button(self.root, image=rounded_send_button_image, command=self.send_file, bd=0)
        send_button.image = rounded_send_button_image
        send_button.pack(pady=10)
        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=10)

    def select_file(self) -> None:
        self.app.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.app.image_path:
            messagebox.showinfo("Selected File", f"Selected: {os.path.basename(self.app.image_path)}")
        else:
            self.app.image_path = None

    def send_file(self) -> None:
        if not self.app.image_path:
            messagebox.showwarning("No File Selected", "Please select a file first.")
            return
        
        self.app.server.file_name = self.app.image_path
        self.app.image_path = None
