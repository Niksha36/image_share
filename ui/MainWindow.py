import tkinter as tk

from ui.utils.rounded_button import create_rounded_rectangle_image


class MainWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_main_window()

    def create_main_window(self) -> None:
        self.app.clear_window()
        tk.Label(self.root, text="Choose Mode", font=("Arial", 20)).pack(pady=20)
        rounded_sender_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Sender", "#FFFFFF", self.app.font)
        sender_button = tk.Button(self.root, image=rounded_sender_button_image, command=self.app.create_sender_window, bd=0)
        sender_button.image = rounded_sender_button_image
        sender_button.pack(pady=10)
        rounded_catcher_button_image = create_rounded_rectangle_image(150, 50, 20, "#FFFFFF", "Catcher", "#000000", self.app.font, "#1a80e5")
        catcher_button = tk.Button(self.root, image=rounded_catcher_button_image, command=self.app.create_server_selection_window, bd=0)
        catcher_button.image = rounded_catcher_button_image
        catcher_button.pack(pady=10)
        