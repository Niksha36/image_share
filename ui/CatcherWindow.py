import ctypes
import os
import subprocess
import tempfile
import threading
import tkinter as tk
import socket
from tkinter import messagebox

from PIL import ImageTk, Image

from client import Client
from ui.utils.rounded_button import create_rounded_rectangle_image


class CatcherWindow:
    def __init__(self, root: tk.Tk, app, server_ip: str):
        self.root = root
        self.app = app
        self.root.geometry("500x450")
        self.server_ip = server_ip
        threading.Thread(target=self.receive_file, daemon=True).start()

        self.prev_image_path = None
        
        self.create_catcher_window()

    def create_catcher_window(self) -> None:
        self.app.clear_window()
        #text view with Catcher Mode text
        tk.Label(self.root, text="Catcher Mode", font=("Arial", 20)).pack(pady=20)
        #image viewer
        self.app.image_label = tk.Label(
            self.root,
            highlightbackground="#339AF0",  # Border color
            highlightcolor="#339AF0",  # Border color when focused
            highlightthickness=3,  # Border thickness
            relief="solid",  # Border style
            text="The image sent by the sender will be here",
            font=("Arial", 12),
        )
        self.app.image_label.pack(padx=40, pady=(0, 5), fill=tk.BOTH, expand=True)

        # set_image_as_background_button button
        rounded_set_as_background_button_image = create_rounded_rectangle_image(
            300, 50, 20, "#1a80e5", "Set image as desktop background", "#FFFFFF", self.app.font
        )
        set_image_as_background_button = tk.Button(
            self.root, image=rounded_set_as_background_button_image, command=self.set_desktop_background, bd=0
        )
        set_image_as_background_button.image = rounded_set_as_background_button_image
        set_image_as_background_button.pack(pady=(5,15))

        #open file location button
        rounded_set_as_background_button_image = create_rounded_rectangle_image(
            300, 50, 20, "#1a80e5", "Open file location", "#FFFFFF", self.app.font
        )
        open_file_location_button = tk.Button(
            self.root, image=rounded_set_as_background_button_image, command=self.open_file_location, bd=0
        )
        open_file_location_button.image = rounded_set_as_background_button_image
        open_file_location_button.pack(pady=(0,20))

        #back button
        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=5)

    def receive_file(self) -> None:
        self.app.client = Client(self.app.chunk_size, self.app.client_name_files)
        try:
            self.app.client.client.connect((self.server_ip, self.app.port))
            self.app.client.client.send(b"ITCLIENT")
        except socket.error:
            messagebox.showwarning("Connection error", "Failed to connect to the server. Please try again later.")
            self.app.go_back()
            return

        if not os.path.exists("received_images"):
            os.makedirs("received_images")

        while self.app.client.client.fileno() != -1:
            try:
                self.app.client.run()
            except Exception as e:
                messagebox.showwarning("Connection to the server was lost.", "Reconnect to the server.")
                self.app.go_back()
                return

            if self.app.client is None: break
            if  self.app.client.is_download:
                self.display_image()
                self.app.count_images += 1
                self.app.client.is_download = False

    def display_image(self) -> None:
        try:
            img = Image.open(self.app.client.image_path)
            label_width = self.app.image_label.winfo_width()
            label_height = 223

            self.prev_image_path = self.app.client.image_path

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
        except:
            self.app.client.image_path = self.prev_image_path
            messagebox.showwarning("Error reading file", "The sender sent an invalid file.")

    def set_desktop_background(self) -> None:
        if self.app.client.image_path:
            try:
                img = Image.open(self.app.client.image_path)

                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.bmp') as tmpfile:
                    bmp_path = tmpfile.name

                # Save the image as BMP
                img.save(bmp_path, 'BMP')

                # Set the desktop background using ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, bmp_path, 3)
            except Exception as e:
                messagebox.showwarning("Error", f"Failed to set desktop background: {e}")
        else:
            messagebox.showwarning("Error", "No images have been received yet.")

    def open_file_location(self) -> None:
        if self.app.client.image_path:
            os.startfile(os.path.realpath(os.curdir) + "\\received_images")
        else:
            messagebox.showwarning("Error", "No images have been received yet.")
