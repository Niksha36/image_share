import os
import webbrowser
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

from server import Server
from ui.utils.rounded_button import create_rounded_rectangle_image


class SenderWindow:
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        
        self.app.server = Server(self.app.file_path, self.app.port)
        threading.Thread(target=self.app.server.accept_clients, daemon=True).start()
        self.create_sender_window()

    def create_sender_window(self) -> None:
        self.app.clear_window()
        tk.Label(self.root, text="Sender Mode", font=("Arial", 20)).pack(pady=7)
        no_image_selected = tk.PhotoImage(file="./drawables/ic_no_image_selected.png")

        self.image_condition_label = tk.Label(self.root, image=no_image_selected)
        self.image_condition_label.image = no_image_selected
        self.image_condition_label.pack()
        self.image_name_label = tk.Label(self.root, text="")
        self.image_name_label.pack_configure(pady=(0, 10))

        rounded_select_file_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Select File", "#FFFFFF", self.app.font)
        select_file_button = tk.Button(self.root, image=rounded_select_file_button_image, command=self.select_file, bd=0)
        select_file_button.image = rounded_select_file_button_image
        select_file_button.pack(pady=5)

        rounded_send_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Send", "#FFFFFF", self.app.font)
        send_button = tk.Button(self.root, image=rounded_send_button_image, command=self.send_file, bd=0)
        send_button.image = rounded_send_button_image
        send_button.pack(pady=10)

        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=10)

    def select_file(self) -> None:
        self.app.file_path = filedialog.askopenfilename(filetypes=[("Documents and Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.pdf;*.doc;*.docx;*.txt")])
        if self.app.file_path:
            file_extension = os.path.splitext(self.app.file_path)[1].lower()
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

            image_selected = tk.PhotoImage(file="./drawables/ic_image_selected.png") if file_extension in image_extensions else tk.PhotoImage(file="./drawables/ic_document_selected.png")
            self.image_condition_label.config(image=image_selected)
            self.image_condition_label.image = image_selected
            messagebox.showinfo("Selected File", f"Selected: {os.path.basename(self.app.file_path)}")

            image_name = os.path.basename(self.app.file_path)
            self.image_name_label.config(text = image_name, font=(self.app.font, 12))
            self.image_condition_label.config(image=image_selected)
            self.image_condition_label.image = image_selected
            self.image_condition_label.bind("<Button-1>", self.open_image)
        else:
            self.app.file_path = None

    def open_image(self, event: tk.Event) -> None:
        def run():
            if self.app.file_path:
                webbrowser.open(self.app.file_path)

        threading.Thread(target=run, daemon=True).start()

    def send_file(self) -> None:
        if not self.app.file_path:
            messagebox.showwarning("No File Selected", "Please select a file first.")
            return
        
        self.app.server.file_path = self.app.file_path
        messagebox.showinfo("Success", "Image was successfully sent")
