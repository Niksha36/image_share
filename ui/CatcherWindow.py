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
        self.root.geometry("500x505")
        self.server_ip = server_ip
        threading.Thread(target=self.receive_file, daemon=True).start()
        self.prev_image = None

        self.active_rounded_set_as_background_button_image = create_rounded_rectangle_image(
            300, 50, 20, "#1a80e5", "Set image as desktop background", "#FFFFFF", self.app.font
        )
        self.active_rounded_open_file_location_button = create_rounded_rectangle_image(
            300, 50, 20, "#1a80e5", "Open file location", "#FFFFFF", self.app.font
        )

        self.inactive_rounded_set_as_background_button_image = create_rounded_rectangle_image(
            300, 50, 20, "#CFCFCF", "Set image as desktop background", "#737373", self.app.font
        )
        self.inactive_rounded_open_file_location_button = create_rounded_rectangle_image(
            300, 50, 20, "#CFCFCF", "Open file location", "#737373", self.app.font
        )

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
        
        self.image_name_label = tk.Label(self.root, text="")
        self.image_name_label.pack(pady=(0, 15))
        # set_image_as_background_button button
        self.set_image_as_background_button = tk.Button(
            self.root, image=self.inactive_rounded_set_as_background_button_image, command=self.set_desktop_background, bd=0
        )
        self.set_image_as_background_button.image = self.inactive_rounded_set_as_background_button_image
        self.set_image_as_background_button.pack(pady=(5,15))

        #open file location button
        self.open_file_location_button = tk.Button(
            self.root, image=self.inactive_rounded_open_file_location_button, command=self.open_file_location, bd=0
        )
        self.open_file_location_button.image = self.inactive_rounded_open_file_location_button
        self.open_file_location_button.pack(pady=(0,20))

        #back button
        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=5)

    def receive_file(self) -> None:
        self.app.client = Client(self.app.chunk_size)
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
                print(e)
                messagebox.showwarning("Connection to the server was lost.", "Reconnect to the server.")
                self.app.go_back()
                return

            if self.app.client is None: break
            if self.app.client.is_download:
                self.display_image()
                self.make_active_open_file_location_button()
                self.app.client.is_download = False
    
    def is_image_file(self, file_path: str) -> bool:
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in image_extensions
        
    def display_image(self) -> None:
        if self.is_image_file(self.app.client.file_path):
            self.image_name_label.config(text="", font=(self.app.font, 14))
            self.make_active_set_desktop_background_button()
            try:
                img = Image.open(self.app.client.file_path)
                self.prev_image = self.app.client.file_path
            except Exception as e:
                print(f"Error: {e}")
                self.app.client.file_path = self.prev_image
                messagebox.showwarning("Error reading file", "The sender sent an invalid file.")
                return

            label_width = self.app.image_label.winfo_width()
            label_height = 223

            img_ratio = img.width / img.height
            label_ratio = label_width / label_height

            if img_ratio > label_ratio:
                new_width = label_width
                new_height = int(label_width / img_ratio)
            else:
                new_height = label_height
                new_width = int(label_height * img_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.app.image_label.config(
                image=img,
                text="",
                width=new_width,
                height=new_height,
                highlightthickness=0,
                relief="flat"
            )
            self.app.image_label.image = img
            self.make_active_set_desktop_background_button()

        else:
            self.make_inactive_set_desktop_background_button()
            doc_img = ImageTk.PhotoImage(file="./drawables/ic_document_selected.png")
            self.app.image_label.config(
                image=doc_img,
                text="",
                width=doc_img.width(),
                height=doc_img.height(),
                highlightthickness=0,
                relief="flat"
            )
            self.app.image_label.image = doc_img
            self.image_name_label.config(text = os.path.basename(self.app.client.file_path), font=(self.app.font, 14))
    def set_desktop_background(self) -> None:
        if self.app.client.file_path and self.is_image_file(self.app.client.file_path):
            try:
                img = Image.open(self.app.client.file_path)

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
        if self.app.client.file_path:
            os.startfile(os.path.realpath(os.curdir) + "\\received_images")
        else:
            messagebox.showwarning("Error", "No files have been received yet.")

    # changing color of Open file location button to active
    def make_active_open_file_location_button(self):
        self.open_file_location_button.config(image=self.active_rounded_open_file_location_button)
        self.open_file_location_button.image = self.active_rounded_open_file_location_button

    def make_active_set_desktop_background_button(self):
        self.set_image_as_background_button.config(image=self.active_rounded_set_as_background_button_image)
        self.set_image_as_background_button.image = self.active_rounded_set_as_background_button_image

    # changing color of Set image as desktop background button to active
    def make_inactive_set_desktop_background_button(self):
        self.set_image_as_background_button.config(image=self.inactive_rounded_set_as_background_button_image)
        self.set_image_as_background_button.image = self.inactive_rounded_set_as_background_button_image

    def make_inactive_open_file_location_button(self):
        self.open_file_location_button.config(image=self.inactive_rounded_open_file_location_button)
        self.open_file_location_button.image = self.inactive_rounded_open_file_location_button