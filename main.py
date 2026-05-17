import tkinter as tk
from src.ui.face_auth_app import FaceAuthApp
from src.ui.loading_screen import LoadingScreen

def start_main_app(root):
    # Clear the window for the main app
    for widget in root.winfo_children():
        widget.destroy()
    app = FaceAuthApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    
    # We optionally can use LoadingScreen or just start the app directly
    # Since original main.py didn't use loading screen actively, we will just launch FaceAuthApp
    # to maintain exactly the same behavior without breaking things.
    app = FaceAuthApp(root)
    root.mainloop()
