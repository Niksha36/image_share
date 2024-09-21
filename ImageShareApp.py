import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import socket
import os
import threading

class ImageShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Share App")
        self.root.geometry("450x350")
        self.mode = None
        self.image_path = None
        self.window_stack = []
        self.receiver_running = False
        self.receiver_thread = None
        self.create_main_window()

    def create_main_window(self):
        self.clear_window()
        tk.Label(self.root, text="Choose Mode", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Sender", command=self.create_sender_window).pack(pady=10)
        tk.Button(self.root, text="Catcher", command=self.create_catcher_window).pack(pady=10)

    def create_sender_window(self):
        self.clear_window()
        tk.Label(self.root, text="Sender Mode", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Select File", command=self.select_file).pack(pady=10)
        tk.Button(self.root, text="Send", command=self.send_file).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)

    def create_catcher_window(self):
        self.clear_window()
        tk.Label(self.root, text="Catcher Mode", font=("Arial", 20)).pack(pady=20)
        self.image_label = tk.Label(self.root, text="The image sent by the sender will be here", font=("Arial", 12), width=40, height=10, relief="solid")
        self.image_label.pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)
        self.receiver_running = True
        self.receiver_thread = threading.Thread(target=self.receive_file, daemon=True)
        self.receiver_thread.start()

    def clear_window(self):
        # Store the current state of the window
        state = []
        for widget in self.root.winfo_children():
            if widget.winfo_manager() == 'pack':
                state.append((widget.pack_info(), widget))
                widget.pack_forget()
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
        # Convert image to RGB if it has an alpha channel
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # Save the image with compression
        compressed_image_path = "compressed_image.jpg"
        img.save(compressed_image_path, "JPEG", quality=30)

        host = 'localhost'  # Change to the receiver's IP address
        port = 5001

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            with open(compressed_image_path, 'rb') as f:
                data = f.read()
                s.sendall(data)
            messagebox.showinfo("Success", "File sent successfully.")

    def receive_file(self):
        host = 'localhost'
        port = 5001

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            while self.receiver_running:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    with open("received_image.jpg", 'wb') as f:
                        while data:
                            f.write(data)
                            data = conn.recv(1024)
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