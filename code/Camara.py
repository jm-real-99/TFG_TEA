import cv2
import dlib
from tensorflow import keras
from Emociones import Emociones
import numpy as np

class Camara:
    def __init__(self,camera):
        # Cargar el modelo pre-entrenado de detección de caras de OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.predictor = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")
        # Cargamos el modelo preentrenado, ver la referencia para saber de dónde lo he sacado (quizás tenga que entrenar yo mismo uno)
        self.model = keras.models.load_model("modelos/model.h5")
        # Inicializamos la cámara web
        self.cap = cv2.VideoCapture(camera)
        ##QUIZAS PODAMOS QUITAR ESTA VARIABLE
        detector = dlib.get_frontal_face_detector()

    def readFrame(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectamos caras en el fotograma
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Dibujamos un rectángulo alrededor de la cara detectada
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Obtenemos los puntos de referencia faciales
            landmarks = self.predictor(gray, dlib.rectangle(x, y, x + w, y + h))

            # Dibujamos los puntos recogidos en landmarks
            for i in range(68):  # 68 puntos de referencia faciales
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Extraemos la región de interés (ROI) y la redimensionamos
            roi = gray[y:y + h, x:x + w]
            resized = cv2.resize(roi, (48, 48))

            # Realizamos la predicción utilizando el modelo cargado
            prediction = self.model.predict(np.array([resized]).reshape(1, 48, 48, 1))[0]

            # vvvvvvvvvvvvvvvvvvvvvv  TRASLADAR A GESTOR EMOCIONES vvvvvvvvvvvvvvvvvvvvvvvvvv
            # Del vector con las probabilidades de emociones, cogemos el más probable.
            print(Emociones.name)
            print(prediction)
            emocion = emociones[np.argmax(prediction)]
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # Agregamos el texto a la imagen
            cv2.putText(frame, emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Detección de Caras', frame)
