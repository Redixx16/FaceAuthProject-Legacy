import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox, ttk, Frame
from src.core.face_utils import FaceUtils
import mediapipe as mp
import time
import json
from datetime import datetime

class FaceAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mahú Perú - Autenticación Facial")
        self.root.geometry("1000x700") 
        self.root.configure(bg="#F7F9FB") 


        self.total_attempts = 0
        self.failed_attempts = 0
        self.successful_attempts = 0
        self.response_times = []

        # Initialize components
        self.face_utils = FaceUtils()
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5
        )

        self.users_data_file = "data/users_data.json"
        self.users_data = self.load_users_data()


        self.create_styles()
        self.create_main_layout()

    def create_styles(self):
        """Create custom styles for an elegant, modern look with more prominent buttons"""
        style = ttk.Style()
        

        primary_color = "#1A5F7A"  
        secondary_color = "#159895" 
        background_color = "#F5F5F5" 
        text_color = "#2C3E50"        
        accent_color = "#57C5B6"     


        style.configure("Custom.TEntry", 
            font=("Segoe UI", 12),
            foreground=text_color,
            background="white",
            fieldbackground="white",
            bordercolor=secondary_color,
            borderwidth=2,
            padding=10
        )


        style.configure("Primary.TButton", 
            font=("Segoe UI Semibold", 14),
            background=accent_color,
            foreground="black",
            padding=10,
            width=15
        )
        style.map("Primary.TButton", 
            background=[('active', secondary_color)],
            foreground=[('active', 'white')]
        )

    def create_main_layout(self):
        """Create a more sophisticated main layout with an elegant color scheme and prominent buttons"""

        primary_color = "#1A5F7A"     
        secondary_color = "#159895"   
        background_color = "#F5F5F5"   
        text_color = "#2C3E50"         
        accent_color = "#57C5B6"      

        main_container = Frame(self.root, bg=background_color)
        main_container.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)


        logo_frame = Frame(main_container, bg=background_color)
        logo_frame.pack(fill=tk.X, pady=(0, 30))

        logo_label = tk.Label(logo_frame, text="MAHÚ_PERÚ - EMPRESA TEXTIL", 
                            font=("Segoe UI Black", 24), 
                            fg=primary_color, 
                            bg=background_color)
        logo_label.pack(side=tk.LEFT)

        subtitle = tk.Label(logo_frame, 
                            text="Sistema de Autenticación Facial", 
                            font=("Segoe UI", 14), 
                            fg=secondary_color, 
                            bg=background_color)
        subtitle.pack(side=tk.RIGHT)


        auth_frame = Frame(main_container, bg="white", 
                        relief=tk.RAISED, 
                        borderwidth=1)
        auth_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        auth_frame.grid_columnconfigure(0, weight=1)
        auth_frame.grid_columnconfigure(1, weight=1)

        left_frame = Frame(auth_frame, bg="white", padx=30, pady=30)
        left_frame.grid(row=0, column=0, sticky="nsew")

        username_label = tk.Label(left_frame, 
                                text="Nombre de Usuario", 
                                font=("Segoe UI Semibold", 14), 
                                bg="white", 
                                fg=text_color)
        username_label.pack(anchor="w", pady=(0, 10))

        self.entry_user = ttk.Entry(left_frame, style="Custom.TEntry", width=30)
        self.entry_user.pack(fill=tk.X, pady=(0, 20))

        button_frame = Frame(left_frame, bg="white")
        button_frame.pack(fill=tk.X)

        register_button = ttk.Button(button_frame, 
                                    text="Registrar Usuario", 
                                    style="Primary.TButton", 
                                    command=self.register_user)
        register_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        login_button = ttk.Button(button_frame, 
                                text="Iniciar Sesión", 
                                style="Primary.TButton", 
                                command=self.show_instructions)
        login_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        right_frame = Frame(auth_frame, bg=background_color, padx=30, pady=30)
        right_frame.grid(row=0, column=1, sticky="nsew")

        info_title = tk.Label(right_frame, 
                            text="Bienvenido a Autenticación Facial", 
                            font=("Segoe UI Semibold", 16), 
                            bg=background_color, 
                            fg=primary_color)
        info_title.pack(anchor="w", pady=(0, 20))

        info_text = tk.Label(right_frame, 
                            text="Nuestro sistema de autenticación facial utiliza\n"
                                "tecnología de vanguardia para verificar su identidad.\n\n"
                                "Características:\n"
                                "• Alta seguridad\n"
                                "• Verificación en tiempo real\n"
                                "• Mínima intervención del usuario", 
                            font=("Segoe UI", 12), 
                            bg=background_color, 
                            fg=text_color, 
                            justify=tk.LEFT)
        info_text.pack(anchor="w")

        footer = tk.Label(main_container, 
                        text="© 2024 Powered by Mahú Perú - Todos los derechos reservados", 
                        font=("Segoe UI", 10), 
                        fg=secondary_color, 
                        bg=background_color)
        footer.pack(side=tk.BOTTOM, pady=(20, 0))

    def load_users_data(self):
        """Cargar los datos de los usuarios desde el archivo JSON"""
        if os.path.exists(self.users_data_file):
            with open(self.users_data_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_users_data(self):
        """Guardar los datos de los usuarios en el archivo JSON"""
        with open(self.users_data_file, 'w') as file:
            json.dump(self.users_data, file, indent=4)

    def register_user(self):
        user_name = self.entry_user.get().strip()
        if not user_name:
            messagebox.showerror("Error", "Por favor, ingresa un nombre de usuario.")
            return
        if user_name in self.users_data:
            messagebox.showerror("Error", "El usuario ya está registrado.")
            return
        
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.users_data[user_name] = {
            "name": user_name,
            "registration_date": registration_date,
            "last_login": None,
            "failed_attempts": 0,
            "successful_logins": 0
        }
        self.save_users_data()
        self.face_utils.capture_and_register_user(user_name)
        messagebox.showinfo("Registro exitoso", f"Usuario {user_name} registrado con éxito.")

    def show_instructions(self):
        """Mostrar un cuadro emergente con las instrucciones antes de la autenticación."""
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instrucciones para Autenticación Facial")
        instructions_window.geometry("500x350")
        instructions_window.config(bg="#FFFFFF")


        label_title = tk.Label(instructions_window, text="Instrucciones para la Autenticación Facial", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#333333")
        label_title.pack(pady=20)


        instructions_text = (
            "1. Asegúrate de estar bien iluminado.\n"
            "2. Coloca tu rostro frente a la cámara.\n"
            "3. Mantén la cámara a la altura de tus ojos.\n"
            "4. Parpadea varias veces para iniciar el proceso.\n"
            "5. Si la autenticación no funciona, intenta nuevamente."
        )
        label_instructions = tk.Label(instructions_window, text=instructions_text, font=("Arial", 12), bg="#FFFFFF", fg="#333333", justify="left")
        label_instructions.pack(pady=10)

        close_button = tk.Button(instructions_window, text="Comenzar Autenticación", font=("Arial", 14), bg="#4CAF50", fg="white",
                                 width=20, height=2, relief="raised", activebackground="#45a049", command=lambda: self.start_authentication(instructions_window))
        close_button.pack(pady=20)

    def start_authentication(self, instructions_window):
        """Cerrar las instrucciones y comenzar la autenticación facial"""
        instructions_window.destroy()

        if not os.path.exists(self.face_utils.svm_model_path) or not os.path.exists(self.face_utils.encoder_path):
            messagebox.showerror("Error", "Modelo no entrenado. Por favor, registra un usuario primero.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return

        blink_count = 0
        blink_required = 5
        frame_count = 0
        ear_threshold = 0.2 

        def calculate_ear(landmarks, indices):
            """Calcula el EAR dado un conjunto de puntos en los ojos.""" 
            left_eye = np.array([[landmarks[i].x, landmarks[i].y] for i in indices])
            A = np.linalg.norm(left_eye[1] - left_eye[5])
            B = np.linalg.norm(left_eye[2] - left_eye[4])
            C = np.linalg.norm(left_eye[0] - left_eye[3])
            return (A + B) / (2.0 * C)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo acceder a la cámara.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)


            frame_with_mesh = frame.copy()

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    self.face_utils.mp_drawing.draw_landmarks(
                        frame_with_mesh,
                        face_landmarks,
                        self.mp_face_mesh.FACEMESH_TESSELATION,
                        self.face_utils.mp_drawing.DrawingSpec(color=(200, 200, 200), thickness=1, circle_radius=0),
                        self.face_utils.mp_drawing.DrawingSpec(color=(200, 200, 200), thickness=1, circle_radius=0)  
                    )

                    # Calcular EAR para ambos ojos
                    left_eye_indices = [33, 160, 158, 133, 153, 144]  # Índices de MediaPipe para el ojo izquierdo
                    right_eye_indices = [362, 385, 387, 263, 373, 380]  # Índices de MediaPipe para el ojo derecho

                    left_ear = calculate_ear(face_landmarks.landmark, left_eye_indices)
                    right_ear = calculate_ear(face_landmarks.landmark, right_eye_indices)
                    ear = (left_ear + right_ear) / 2.0

                    # Verificar parpadeo
                    if ear < ear_threshold:
                        frame_count += 1
                    else:
                        if frame_count > 3:  # Detecta parpadeo solo si los ojos permanecen cerrados por algunos cuadros
                            blink_count += 1
                            frame_count = 0

                    cv2.putText(frame_with_mesh, f"Parpadeos: {blink_count}/{blink_required}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    if blink_count >= blink_required:
                        start_time = time.time()  # Inicia el cronómetro para medir la velocidad de respuesta

                        faces = self.face_utils.detect_faces(frame)
                        if faces:
                            user, confidence = self.face_utils.authenticate_user(faces[0][1], threshold=0.8)
                            if user != "Desconocido":
                                # Actualizar los datos de login
                                self.users_data[user]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                self.users_data[user]["successful_logins"] += 1
                                self.successful_attempts += 1
                                response_time = time.time() - start_time
                                self.response_times.append(response_time)  # Guardar el tiempo de respuesta
                                self.total_attempts += 1

                                # Mostrar mensaje de bienvenida
                                messagebox.showinfo("Bienvenido", f"Bienvenido {user}")
                                cap.release()
                                cv2.destroyAllWindows()
                                self.show_performance_graph()  # Mostrar el gráfico de desempeño
                                return
                        messagebox.showerror("Error", "Usuario desconocido o parpadeos insuficientes.")
                        self.failed_attempts += 1
                        self.total_attempts += 1
                        self.show_performance_graph()  # Mostrar el gráfico de desempeño
                        break

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:    
                        face_points = [
                            1, 33, 61, 291, 199, 17, 46, 53, 127, 30, 8, 9, 10, 152, 263, 373, 386
                        ]
                        
                        x_points = [face_landmarks.landmark[i].x for i in face_points]
                        y_points = [face_landmarks.landmark[i].y for i in face_points]

                        x_min = int(min(x_points) * frame.shape[1])
                        y_min = int(min(y_points) * frame.shape[0])
                        x_max = int(max(x_points) * frame.shape[1])
                        y_max = int(max(y_points) * frame.shape[0])

                        height = y_max - y_min

                        center_x = (x_min + x_max) // 2
                        center_y = (y_min + y_max) // 2

                        square_size = height  

                        x_min_square = int(center_x - square_size / 2)
                        x_max_square = int(center_x + square_size / 2)
                        y_min_square = int(center_y - square_size / 2)
                        y_max_square = int(center_y + square_size / 2)

                        x_min_square = max(0, x_min_square)
                        y_min_square = max(0, y_min_square)
                        x_max_square = min(frame.shape[1], x_max_square)
                        y_max_square = min(frame.shape[0], y_max_square)

                        cv2.rectangle(frame_with_mesh, (x_min_square, y_min_square), (x_max_square, y_max_square), (0, 255, 0), 2)


                cv2.imshow("Autenticación Facial", frame_with_mesh)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    print("Autenticación interrumpida por el usuario.")
                    break

        cap.release()
        cv2.destroyAllWindows()
    
    def show_performance_graph(self):
        if self.total_attempts == 0:
            messagebox.showwarning("Advertencia", "No se han registrado intentos de autenticación.")
            return

        # Calcular tasas de éxito y error
        success_rate = (self.successful_attempts / self.total_attempts) * 100
        error_rate = (self.failed_attempts / self.total_attempts) * 100

        # Calcular tiempo promedio de respuesta
        avg_response_time = np.mean(self.response_times) if self.response_times else 0

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))

        # Mostrar las métricas
        ax.bar(["Tasa de Éxito", "Tasa de Error"], [success_rate, error_rate], color=["green", "red"])
        ax.set_ylabel("Porcentaje (%)")
        ax.set_title("Métricas de Desempeño del Sistema de Autenticación Facial")

        # Mostrar la barra de tiempo de respuesta
        ax2 = ax.twinx()
        ax2.plot(["Tiempo Promedio de Respuesta"], [avg_response_time], marker="o", color="blue", label="Tiempo Promedio de Respuesta")
        ax2.set_ylabel("Tiempo (segundos)", color="blue")
        ax2.tick_params(axis='y', labelcolor="blue")

        # Mostrar el gráfico
        plt.show()


