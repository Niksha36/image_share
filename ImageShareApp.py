import ctypes
import os
import sys
import threading
import tkinter as tk

import pystray
from PIL import Image, ImageTk, ImageFont

from ui.CatcherWindow import CatcherWindow
from ui.EnterUserNameWindow import EnterUserNameWindow
from ui.MainWindow import MainWindow
from ui.SenderWindow import SenderWindow
from ui.ServerSelectionWindow import ServerSelectionWindow

class ImageShareApp:
    def __init__(self, root: tk.Tk, port: int):
        self.root = root
        self.root.title("Image Share App")
        self.root.geometry("450x350")

        # Load and set the icon
        icon_path = self.resource_path("app_icon.png", "drawables")
        icon_image = ImageTk.PhotoImage(file=icon_path)
        self.root.iconphoto(False, icon_image)
        # Set the taskbar icon
        self.set_taskbar_icon(icon_path)

        self.window_stack = []
        self.font_path = self.resource_path("Roboto-Regular.ttf", "fonts")
        self.font = ImageFont.truetype(self.font_path, 16)

        # Load the back arrow icon
        back_icon_path = self.resource_path("icon_back.png", "drawables")
        self.back_icon_image = ImageTk.PhotoImage(file=back_icon_path)
        
        self.port = port
        self.chunk_size = 8192
        self.file_path = None

        self.client = None
        self.server = None
        self.server_name = None

        self.create_main_window()

    def resource_path(self, relative_path: str, folder: str = None) -> None:
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.join(os.path.abspath("."), folder) if folder else os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def set_taskbar_icon(self, icon_path) -> None:
        icon_image = Image.open(icon_path)
        icon = pystray.Icon("ImageShareApp", icon_image)

        # Set the taskbar icon using ctypes
        # Change this to your app's unique identifier
        myappid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        def run_icon():
            icon.run()

        threading.Thread(target=run_icon, daemon=True).start()

    #логика создания главного окна
    def create_main_window(self) -> None:
        MainWindow(self.root, self)

    #Логика создание sender окна
    def create_sender_window(self) -> None:
        SenderWindow(self.root, self)

    # Логика создание catcher окна
    def create_catcher_window(self, server_ip: str) -> None:
        CatcherWindow(self.root, self, server_ip)

    # Логика окна выбора сервера
    def create_server_selection_window(self) -> None:
        ServerSelectionWindow(self.root, self)

    # Логика окна выбора имени пользователя
    def create_user_selection_window(self) -> None:
        EnterUserNameWindow(self.root, self)

    # функция отчищающая окно
    def clear_window(self) -> None:
        for widget in self.root.winfo_children():
            widget.pack_forget() if widget.winfo_manager() == 'pack' else widget.place_forget()

    def go_back(self) -> None:
        if self.server:
            self.server.close_server()
            self.server = None  # Ensure the server is set to None after closing
        if self.client:
            self.client.close_client()
            self.client = None  # Ensure the client is set to None after closing

        self.file_path = None
        self.create_main_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageShareApp(root, 5050)
    root.mainloop()
