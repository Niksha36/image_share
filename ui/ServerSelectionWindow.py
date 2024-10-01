import time
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

from ui.utils.rounded_button import create_rounded_rectangle_image
from brute_force_ip import BruteForceIp


class ServerSelectionWindow:
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        self.root.geometry("450x350")

        self.searcher = BruteForceIp()
        self.client_ip = socket.gethostbyname(socket.gethostname())
        
        self.previous_ips = set()
        self.selected_item = None
        self.server_name = None
        self.is_search = True

        self.check_mark_image = ImageTk.PhotoImage(Image.open(r".\drawables\ic_check_mark.png"))
        self.wifi_icon_image = ImageTk.PhotoImage(Image.open(r".\drawables\ic_wifi.png").resize((30, 30)))
        self.create_ui()

    def create_ui(self) -> None:
        self.app.clear_window()
        
        threading.Thread(target=self.get_servers, daemon=True).start()

        main_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.pack_propagate(False)  # Prevent the frame from resizing

        label = ttk.Label(main_frame, text="Select a Server", font=("Arial", 20))
        label.pack(pady=10)

        # Create a frame to contain the canvas and scrollbar
        canvas_container = ttk.Frame(main_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))  # Add padding to move the scroll view down

        self.canvas = tk.Canvas(canvas_container, height=200)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=scrollbar.set)

        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.canvas_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Add padding at the bottom of the canvas_frame
        spacer = ttk.Frame(self.canvas_frame, height=50)
        spacer.pack(fill=tk.X)

        self.canvas_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        self.rounded_submit_button_image = create_rounded_rectangle_image(150, 50, 20, "#1a80e5", "Submit", "#FFFFFF")
        submit_button = tk.Button(button_frame, image=self.rounded_submit_button_image, bd=0, command=self.on_submit)
        submit_button.pack()

        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.go_back, bd=0)
        back_button.place(x=3, y=0)

        threading.Thread(target=self.get_servers, daemon=True).start()

    def on_frame_configure(self, event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def select_server(self, index: int, server_name: str) -> None:
        if self.selected_item is not None:
            self.canvas.delete(f"check_{self.selected_item}")
            if self.selected_item == index:
                self.selected_item = None
                self.connect_server = None
                return

        self.selected_item = index
        self.connect_server = server_name
        x1, y1, x2, y2 = self.canvas.bbox(f"text_{index}")
        self.canvas.create_image(x2 + 20, (y1 + y2) // 2, image=self.check_mark_image, tags=f"check_{index}")
    
    def get_servers(self) -> None:        
        while self.is_search :
            self.searcher.search(self.client_ip, self.app.port)
            new_ips = self.searcher.ip_adresses
            print(new_ips)

            if new_ips and new_ips != self.previous_ips:
                self.previous_ips = new_ips
                self.canvas.delete("all")  # Clear the canvas before adding new items
                for index, server_ip in enumerate(self.previous_ips):
                    self.canvas.create_image(10, 30 * index + 20, anchor="w", image=self.wifi_icon_image,
                                             tags=f"icon_{index}")
                    self.canvas.create_text(50, 30 * index + 20, anchor="w", text=self.previous_ips[server_ip], font=("Arial", 16),
                                            tags=f"text_{index}")
                    self.canvas.tag_bind(f"text_{index}", "<Button-1>",
                                         lambda e, i=index: self.select_server(i, server_ip))
            time.sleep(1)

    def on_submit(self) -> None:
        if self.connect_server:
            print(f"Selected server: {self.connect_server}")
            self.is_search = False
            self.app.create_catcher_window(self.connect_server)
        else:
            messagebox.showwarning("No Server Selected", "Please select a server to continue")
    
    def go_back(self) -> None:
        self.is_search  = False
        self.app.go_back()
