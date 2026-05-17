# FaceAuthProject

Face Authentication System with Liveness Detection. 

This project was developed for the Intelligent Systems and Machine Learning course. It uses MediaPipe, OpenCV, DeepFace, and an SVM model to authenticate users securely while detecting if the user is real (blink detection) to prevent spoofing.

## Features
- **Face Registration:** Automatically extract embeddings from the camera.
- **Liveness Detection:** Analyzes eye blinks in real-time to avoid picture/video spoofing.
- **Face Authentication:** Validates identity against an SVM trained on DeepFace embeddings.
- **Interactive GUI:** Built with Tkinter, featuring an elegant, modern visual interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Redixx16/FaceAuthProject.git
   cd FaceAuthProject
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On Mac/Linux
   source env/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main application:
```bash
python main.py
```
