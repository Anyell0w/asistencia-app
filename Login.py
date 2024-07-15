import tkinter as tk
from tkinter import messagebox as mb


class Login:
    def __init__(self, root):
        self.root = root
        self.root.resizable(0, 0)
        self.root.configure(bg="black")
        self.root.iconbitmap("./images/Logo_UNAP.ico")
        self.root.geometry("540x250")
        self.root.title("Login")
        self.lbl1 = tk.Label(self.root, text="Usuario", bg="white")
        self.lbl1.pack()
        self.lbl1.place(x=10, y=10)
        self.lbl2 = tk.Label(self.root, text="Contraseña", bg="white")
        self.lbl2.pack()
        self.lbl2.place(x=10, y=40)
        self.entry1 = tk.Entry(self.root, width=20)
        self.entry1.pack()
        self.entry1.place(x=100, y=10)
        self.entry2 = tk.Entry(self.root, width=20)
        self.entry2.pack()
        self.entry2.place(x=100, y=40)
        self.button = tk.Button(self.root, text="Login", command=self.login, font="Helvetica 12")
        self.button.pack()
        self.button.place(x=227, y=70)
        self.button.config(bg="white", fg="black", padx=10,
                           font="Sans 12", relief="solid", foreground="black",
                           activebackground="white")
        self.lbl1.config(bg="black", fg="white", padx=10,
                         relief="solid", font="Helvetica 12")
        self.lbl2.config(bg="black", fg="white", padx=10,
                         relief="solid", font="Helvetica 12")
        self.entry1.config(show="", font="Helvetica 12", bd=2)
        self.entry2.config(show="*", font="Helvetica 12", bd=2)
        self.entry1.place(x=110)
        self.entry2.place(x=110)

        # imagen
        self.image = tk.PhotoImage(file="./images/images.png")
        self.label = tk.Label(self.root, image=self.image)
        self.label.pack()
        self.label.place(x=300, y=10)

    def login(self, admin_window):
        username = self.entry1.get()
        password = self.entry2.get()
        if username == "admin" and password != "admin":
            mb.showerror("Login", "ADMIN")
            admin_window()
        else:
            mb.showerror("Login", "Usuario o contraseña incorrectos")
