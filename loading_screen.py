import tkinter as tk
from tkinter import ttk

class LoadingScreen:
    def __init__(self, root, main_app_callback):
        self.root = root
        self.main_app_callback = main_app_callback

        # Configuración de la ventana de carga
        self.root.title("Cargando...")
        self.root.geometry("600x400")
        self.root.config(bg="#2C3E50")
        self.root.resizable(False, False)

        # Fondo de la pantalla de carga
        self.bg_frame = tk.Frame(self.root, bg="#2C3E50", width=600, height=400)
        self.bg_frame.place(x=0, y=0)

        # Texto de carga
        self.loading_label = tk.Label(
            self.bg_frame,
            text="Cargando la aplicación...",
            font=("yu gothic ui", 20),
            fg="#FFFFFF",
            bg="#2C3E50",
        )
        self.loading_label.place(x=150, y=100)

        # Barra de progreso
        self.progress = ttk.Progressbar(
            self.bg_frame,
            orient="horizontal",
            length=400,
            mode="indeterminate",
            style="TProgressbar",
        )
        self.progress.place(x=100, y=200)
        self.progress.start()

        # Iniciar el proceso de carga
        self.start_loading_process()

    def start_loading_process(self):
        """Simula el proceso de carga sin bloquear la interfaz."""
        # Después de un pequeño retraso, llamamos a la función que inicializa la ventana principal.
        self.root.after(3000, self.complete_loading)  # Esperamos 3 segundos para cerrar

    def complete_loading(self):
        """Llama al callback para cargar la ventana principal y cierra la pantalla de carga."""
        # Llamamos al callback para iniciar la ventana principal
        self.main_app_callback()

        # Cerrar la ventana de carga después de 3 segundos
        self.root.destroy()  # Destruir la ventana de carga
        self.root.quit()  # Terminar el bucle de eventos de la ventana de carga
