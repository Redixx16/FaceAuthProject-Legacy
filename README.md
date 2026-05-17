# Sistema de Autenticación Facial - Mahú Perú

Proyecto de sistema de autenticación facial con detección de vida (liveness detection) diseñado para implementarse en el control de acceso de personal.

## Arquitectura del Proyecto

El proyecto está organizado bajo los principios de Clean Architecture para asegurar escalabilidad y separación de responsabilidades:

```text
FaceAuthProject/
├── src/                        # Código fuente principal
│   ├── ui/                     # Componentes de interfaz gráfica (Tkinter)
│   └── core/                   # Lógica de negocio, procesamiento facial y utilidades
├── scripts/                    # Scripts independientes (ej. entrenamiento manual)
├── models/                     # Modelos de Machine Learning entrenados (.pkl, .xml)
├── data/                       # Almacenamiento local de la aplicación
│   ├── dataset/                # Imágenes de rostros extraídas
│   └── users_data.json         # Registro de logs de sesiones
├── main.py                     # Entry point de la aplicación
└── requirements.txt            # Dependencias del proyecto
```

## Características
- **Clean Architecture:** Código modular separado en Lógica de Interfaz (`src/ui`) y Lógica de Negocio (`src/core`).
- **Registro de Rostros:** Extracción de embeddings (vectores de características) usando MediaPipe y TensorFlow Hub.
- **Liveness Detection:** Cálculo del EAR (Eye Aspect Ratio) en tiempo real para evitar falsificaciones (anti-spoofing) mediante fotos o videos.
- **Clasificación SVM:** Autenticación rápida de identidad usando un modelo de Support Vector Machine entrenado sobre los embeddings extraídos.

## Requisitos y Configuración

1. Clonar el repositorio y acceder a la carpeta:
   ```bash
   git clone https://github.com/Redixx16/FaceAuthProject.git
   cd FaceAuthProject
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv env
   .\env\Scripts\activate      # Windows
   source env/bin/activate     # Mac/Linux
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Para iniciar la aplicación visual, ejecuta:
```bash
python main.py
```
Para forzar el entrenamiento manual del modelo con el dataset local:
```bash
python scripts/train_model.py
```
