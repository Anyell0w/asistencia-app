import tkinter as tk
from attendance_app import AttendanceApp
from Login import Login

if __name__ == "__main__":
    root = tk.Tk()
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8"
    app = AttendanceApp(root, './usuarios.db', api_token)
    root.mainloop()
