import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import socket
import os
import threading
import ctypes
import pystray
import sys


def create_rounded_rectangle_image(width, height, radius, fill_color, text, text_color, font, border=None):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw rounded rectangle
    draw.rounded_rectangle((0, 0, width, height), radius, fill=fill_color)

    if border is not None:
        draw.rounded_rectangle((0, 0, width, height), radius, outline=border, width=3)
    # Draw text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return ImageTk.PhotoImage(image)


class ImageShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Share App")
        self.root.geometry("450x350")

        # Load and set the icon
        icon_path = os.path.join(os.path.dirname(__file__), "drawables", "app_icon.png")
        icon_image = ImageTk.PhotoImage(file=icon_path)
        self.root.iconphoto(False, icon_image)
        # Set the taskbar icon
        self.set_taskbar_icon(icon_path)

        self.mode = None
        self.image_path = None
        self.window_stack = []
        self.receiver_running = False
        self.receiver_thread = None
        self.font_path = self.resource_path('fonts/Roboto-Regular.ttf')
        self.font = ImageFont.truetype(self.font_path, 16)
        # Load the back arrow icon
        back_icon_path = os.path.join(os.path.dirname(__file__), "drawables", "icon_back.png")
        self.back_icon_image = ImageTk.PhotoImage(file=back_icon_path)
        self.create_main_window()

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def set_taskbar_icon(self, icon_path):
        # Load the icon image
        icon_image = Image.open(icon_path)
        icon = pystray.Icon("ImageShareApp", icon_image)

        # Set the taskbar icon using ctypes
        myappid = 'mycompany.myproduct.subproduct.version'  # Change this to your app's unique identifier
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        def run_icon():
            icon.run()

        icon_thread = threading.Thread(target=run_icon, daemon=True)
        icon_thread.start()

    def create_main_window(self):
        self.clear_window()
        tk.Label(self.root, text="Choose Mode", font=("Arial", 20)).pack(pady=20)
        # Create the rounded rectangle image

        rounded_sender_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Sender", "#FFFFFF", self.font)

        # Create the Sender button with the rounded image
        sender_button = tk.Button(self.root, image=rounded_sender_button_image, command=self.create_sender_window, bd=0)
        sender_button.image = rounded_sender_button_image  # Keep a reference to avoid garbage collection
        sender_button.pack(pady=10)

        rounded_catcher_button_image = create_rounded_rectangle_image(150, 50, 20, "#FFFFFF", "Catcher", "#000000",
                                                                      self.font, "#1a80e5")
        catcher_button = tk.Button(self.root, image=rounded_catcher_button_image, command=self.create_catcher_window,
                                   bd=0)
        catcher_button.image = rounded_catcher_button_image
        catcher_button.pack(pady=10)

    def create_sender_window(self):
        self.clear_window()
        tk.Label(self.root, text="Sender Mode", font=("Arial", 20)).pack(pady=20)
        rounded_select_file_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Select File",
                                                                          "#FFFFFF", self.font)

        # Create the "Select File" button with the rounded image
        select_file_button = tk.Button(self.root, image=rounded_select_file_button_image, command=self.select_file, bd=0)
        select_file_button.image = rounded_select_file_button_image  # Keep a reference to avoid garbage collection
        select_file_button.pack(pady=10)

        # Create the rounded rectangle image for the "Send" button
        rounded_send_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Send", "#FFFFFF", self.font)
        # Create the "Send" button with the rounded image
        send_button = tk.Button(self.root, image=rounded_send_button_image, command=self.send_file, bd=0)
        send_button.image = rounded_send_button_image  # Keep a reference to avoid garbage collection
        send_button.pack(pady=10)
        back_button = tk.Button(self.root, image=self.back_icon_image, command=self.go_back, bd=0)
        back_button.place(x=10, y=10)

    def create_catcher_window(self):
        self.clear_window()
        tk.Label(self.root, text="Catcher Mode", font=("Arial", 20)).pack(pady=20)
        self.image_label = tk.Label(self.root, text="The image sent by the sender will be here", font=("Arial", 12),
                                    width=40, height=10, relief="solid")
        self.image_label.pack(pady=10)
        back_button = tk.Button(self.root, image=self.back_icon_image, command=self.go_back, bd=0)
        back_button.place(x=10, y=10)
        self.receiver_running = True
        self.receiver_thread = threading.Thread(target=self.receive_file, daemon=True)
        self.receiver_thread.start()

    def clear_window(self):
        # Store the current state of the window
        state = []
        for widget in self.root.winfo_children():
            if widget.winfo_manager() == 'pack' or widget.winfo_manager() == 'place':
                state.append((widget.pack_info() if widget.winfo_manager() == 'pack' else widget.place_info(), widget))
                widget.pack_forget() if widget.winfo_manager() == 'pack' else widget.place_forget()
        self.window_stack.append(state)

    def go_back(self):
        self.receiver_running = False
        if self.window_stack:
            state = self.window_stack.pop()
            self.clear_window()  # Clear the current window before restoring the previous state
            for pack_info, widget in state:
                widget.pack(**pack_info)
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button):
                    if widget.cget('text') == 'Sender':
                        widget.config(command=self.create_sender_window)
                    elif widget.cget('text') == 'Catcher':
                        widget.config(command=self.create_catcher_window)
                    elif widget.cget('text') == 'Select File':
                        widget.config(command=self.select_file)
                    elif widget.cget('text') == 'Send':
                        widget.config(command=self.send_file)
                    elif widget.cget('text') == 'Back':
                        widget.config(command=self.go_back)

    def select_file(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            messagebox.showinfo("Selected File", f"Selected: {os.path.basename(self.image_path)}")

    def send_file(self):
        if not self.image_path:
            messagebox.showwarning("No File Selected", "Please select a file first.")
            return

        img = Image.open(self.image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        compressed_image_path = "compressed_image.jpg"
        img.save(compressed_image_path, "JPEG", quality=50)

        port = 5001
        broadcast_ip = '<broadcast>'
        chunk_size = 4096  # Define the chunk size
        end_of_transmission = b'END_OF_TRANSMISSION'

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                with open(compressed_image_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        s.sendto(chunk, (broadcast_ip, port))
                s.sendto(end_of_transmission, (broadcast_ip, port))  # Send end-of-transmission message
                messagebox.showinfo("Success", "File sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send file: {e}")

    def receive_file(self):
        port = 5001
        received_data = bytearray()
        end_of_transmission = b'END_OF_TRANSMISSION'

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', port))
            while self.receiver_running:
                chunk, addr = s.recvfrom(4096)
                if chunk == end_of_transmission:
                    break
                received_data.extend(chunk)
            with open("received_image.jpg", 'wb') as f:
                f.write(received_data)
            self.display_image("received_image.jpg")

    def display_image(self, image_path):
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img, text="", width=img.width(), height=img.height())
        self.image_label.image = img


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageShareApp(root)
    root.mainloop()
