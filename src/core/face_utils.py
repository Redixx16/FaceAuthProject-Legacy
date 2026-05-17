import cv2
import numpy as np
import os
import tensorflow as tf
import tensorflow_hub as hub
import mediapipe as mp
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import joblib

class FaceUtils:
    def __init__(self, svm_model_path='models/face_recognition_svm.pkl', encoder_path='models/label_encoder.pkl', dataset_path='data/dataset'):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        
        try:
            print("Cargando modelo de extracción de características desde TensorFlow Hub...")
            self.embedding_model = hub.KerasLayer(
                "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4",
                input_shape=(224, 224, 3),
                trainable=False
            )
            print("Modelo de extracción de características cargado exitosamente.")
        except Exception as e:
            print(f"Ocurrió un error al cargar el modelo de extracción de características: {e}")
            raise
        
        self.dataset_path = dataset_path
        self.svm_model_path = svm_model_path
        self.encoder_path = encoder_path

    def detect_faces(self, frame):
        """
        Detecta rostros en un frame utilizando MediaPipe Face Detection.
        Devuelve una lista de cuadros delimitadores y las imágenes recortadas de los rostros.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                # Extraer la caja delimitadora
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x1 = int(bboxC.xmin * iw)
                y1 = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)
                x2 = x1 + w
                y2 = y1 + h

                # Asegurar que las coordenadas estén dentro de los límites de la imagen
                x1, y1 = max(x1, 0), max(y1, 0)
                x2, y2 = min(x2, iw), min(y2, ih)

                face = frame[y1:y2, x1:x2]
                if face.size == 0:
                    print("Advertencia: El rostro recortado está vacío.")
                    continue
                try:
                    face_resized = cv2.resize(face, (224, 224)) 
                    face_normalized = face_resized.astype('float32') / 255.0
                    faces.append(((x1, y1, x2, y2), face_normalized))
                except Exception as e:
                    print(f"Error al redimensionar el rostro: {e}")
                    continue
        else:
            print("No se detectó ningún rostro en el frame.")
        return faces

    def get_face_embedding(self, face_image):
        """
        Genera un embedding para una imagen de rostro utilizando MobileNetV2.
        """
        try:
            # Añadir dimensión de batch
            face_expanded = np.expand_dims(face_image, axis=0) 
            # Obtener el embedding
            embedding = self.embedding_model(face_expanded)
            return embedding.numpy()[0]
        except Exception as e:
            print(f"Error al generar el embedding: {e}")
            return None

    def load_dataset(self):
        """
        Carga el dataset de usuarios y genera los embeddings correspondientes.
        """
        X, y = [], []
        for user in os.listdir(self.dataset_path):
            user_path = os.path.join(self.dataset_path, user)
            if os.path.isdir(user_path):
                for image_name in os.listdir(user_path):
                    image_path = os.path.join(user_path, image_name)
                    img = cv2.imread(image_path)
                    if img is not None:
                        faces = self.detect_faces(img)
                        if len(faces) > 0:
                            face = faces[0][1]  # Tomar el primer rostro detectado
                            embedding = self.get_face_embedding(face)
                            if embedding is not None:
                                X.append(embedding)
                                y.append(user)
                                print(f"Embedding generado para {image_path}: {embedding.shape}")
                            else:
                                print(f"No se pudo obtener el embedding para la imagen: {image_path}")
                        else:
                            print(f"No se detectó rostro en la imagen: {image_path}")
                    else:
                        print(f"No se pudo cargar la imagen: {image_path}")
        print(f"Total de embeddings generados: {len(X)}")
        return np.array(X), np.array(y)

    def train_model(self):
        """
        Entrena el modelo SVM con los embeddings generados del dataset.
        """
        X, y = self.load_dataset()
        if len(X) == 0 or len(y) == 0:
            print("Error: No se generaron embeddings. Verifica que las imágenes en 'dataset' sean válidas y contengan rostros.")
            return
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        clf = SVC(kernel='linear', probability=True)
        clf.fit(X, y_encoded)
        joblib.dump(clf, self.svm_model_path)
        joblib.dump(label_encoder, self.encoder_path)
        print("Modelo de reconocimiento facial entrenado y guardado.")

    def authenticate_user(self, face_image, threshold=0.8):
        """
        Autentica un usuario basado en la imagen de su rostro.
        Retorna el nombre del usuario y la confianza de la predicción.
        """
        if not os.path.exists(self.svm_model_path) or not os.path.exists(self.encoder_path):
            raise FileNotFoundError("El modelo o el codificador de etiquetas no existen. Por favor, entrena el modelo primero.")

        clf = joblib.load(self.svm_model_path)
        label_encoder = joblib.load(self.encoder_path)
        embedding = self.get_face_embedding(face_image)
        if embedding is None:
            print("Error: No se pudo obtener el embedding para la autenticación.")
            return "Desconocido", 0.0

        try:
            prediction = clf.predict([embedding])
            proba = clf.predict_proba([embedding])[0]
            confidence = max(proba)
            user = label_encoder.inverse_transform(prediction)[0]
        except Exception as e:
            print(f"Error durante la predicción con SVM: {e}")
            return "Desconocido", 0.0

        if confidence < threshold:
            return "Desconocido", confidence
        return user, confidence

    def capture_and_register_user(self, user_name, num_images=20):
        """
        Captura imágenes desde la cámara, detecta rostros, guarda imágenes completas y recortadas,
        y entrena el modelo SVM.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        user_folder = os.path.join(self.dataset_path, user_name)
        os.makedirs(user_folder, exist_ok=True)

        count = 0
        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo acceder a la cámara.")
                break

            faces = self.detect_faces(frame)
            if len(faces) > 0:
                for (box, face) in faces:
                    x1, y1, x2, y2 = box
                    # Dibujar el rectángulo verde alrededor del rostro
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Guardar la imagen completa
                    full_image_path = os.path.join(user_folder, f"{user_name}_full_{count}.jpg")
                    try:
                        cv2.imwrite(full_image_path, frame)  # Guarda la imagen completa
                        print(f"Imagen completa guardada: {full_image_path}")
                    except Exception as e:
                        print(f"Error al guardar la imagen completa {full_image_path}: {e}")
                        continue

                    # Guardar el rostro recortado
                    cropped_face_path = os.path.join(user_folder, f"{user_name}_{count}.jpg")
                    try:
                        face_uint8 = (face * 255.0).astype('uint8')  # Convertir de 0-1 a 0-255
                        cv2.imwrite(cropped_face_path, face_uint8)  # Guarda el rostro recortado
                        print(f"Rostro recortado guardado: {cropped_face_path}")
                    except Exception as e:
                        print(f"Error al guardar el rostro recortado {cropped_face_path}: {e}")
                        continue

                    count += 1
                    cv2.putText(frame, f"Captured {count}/{num_images}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.imshow("Capturando imágenes para registro", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        print(f"Captura de imágenes completada. Total de imágenes: {count}")
        self.train_model()  # Entrenar el modelo con las nuevas imágenes

