import tkinter as tk
from tkinter import ttk, messagebox
from ui.SenderWindow import SenderWindow
from ui.utils.rounded_button import create_rounded_rectangle_image


class EnterUserNameWindow:
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        self.root.geometry("450x350")
        self.root.title("Enter Username")
        self.create_ender_user_name_ui()


    def create_ender_user_name_ui(self):
        self.app.clear_window()
        self.style = ttk.Style()
        self.style.configure("TEntry", padding=10, relief="flat", borderwidth=2, foreground="grey")
        self.style.map("TEntry",
                       fieldbackground=[('!focus', 'lightgrey'), ('focus', 'white')],
                       bordercolor=[('focus', 'grey')])

        self.label = tk.Label(self.root, text="Enter username", font=(self.app.font, 20))
        self.label.pack(pady=(25, 40))

        self.username_entry = ttk.Entry(self.root, font=(self.app.font, 14), style="TEntry")
        self.username_entry.pack(pady=10, ipadx=10, ipady=10)
        self.username_entry.insert(0, "username")
        self.username_entry.bind("<FocusIn>", self.clear_placeholder)
        self.username_entry.bind("<FocusOut>", self.add_placeholder)

        rounded_submit_button_image = create_rounded_rectangle_image(260, 50, 20, "#1a80e5", "Submit", "#FFFFFF",
                                                                     font=self.app.font)
        submit_button = tk.Button(self.root, image=rounded_submit_button_image, command=self.submit_username,
                                  bd=0)
        submit_button.image = rounded_submit_button_image
        submit_button.pack(pady=10)
        
        back_button = tk.Button(self.root, image=self.app.back_icon_image, command=self.app.go_back, bd=0)
        back_button.place(x=10, y=10)

    def clear_placeholder(self, event):
        if self.username_entry.get() == "username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(foreground="black")

    def add_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "username")
            self.username_entry.config(foreground="grey")

    def submit_username(self):
        self.username = self.username_entry.get()
        if self.username == "username":
            username = ""

        if self.is_user_name_correct(self.username):
            self.app.server_name = self.username
            self.app.create_sender_window()
        else:
            messagebox.showwarning("Incorrect username", "Username length should be greater than 3 and contain only letters.")

    def is_user_name_correct(self, userName):
        if len(userName) >= 3 and userName.isalpha():
            if userName.lower() in ["mesenev", "месенев", "месенёв"]:
                messagebox.showwarning("Это же.....", "Добро пожаловать, Великий и Могучий Месенёв!!!!")
            return True
        return False
