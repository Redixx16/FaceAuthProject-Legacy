from face_utils import train_model, model

DATASET_PATH = "dataset"

if model is None:
    print("Error: El modelo facenet_keras.h5 no se cargó correctamente. Verifica el archivo.")
else:
    train_model(DATASET_PATH)
