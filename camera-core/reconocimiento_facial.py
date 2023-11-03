import cv2
import dlib
import tensorflow as tf
from tensorflow import keras
import numpy as np

emociones = ['angry','disgusted','fearful','happy','sad','surprised','neutral']
# Cargar el modelo pre-entrenado de detección de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")

#Cargamos el modelo preentrenado, ver la referencia para saber de dónde lo he sacado (quizás tenga que entrenar yo mismo uno)
model = keras.models.load_model("modelos/model.h5")

# Inicializar la cámara web
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Dibujar un rectángulo alrededor de la cara detectada
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Obtener los puntos de referencia faciales
        landmarks = predictor(gray, dlib.rectangle(x, y, x+w, y+h))

        # Dibujamos los puntos recogidos en landmarks
        for i in range(68):  # 68 puntos de referencia faciales
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Extraer la región de interés (ROI) y redimensionarla
    roi = gray[y:y + h, x:x + w]
    resized = cv2.resize(roi, (48, 48))

    # Realizar la predicción utilizando el modelo
    prediction = model.predict(np.array([resized]).reshape(1, 48, 48, 1))[0]

    # devuelve un vector con la probabilidad de que la imagen de entrada muestre cada una de las emociones anteriores
    emocion = emociones[np.argmax(prediction)]
    #print(emocion)
    # Agregar el texto a la imagen
    cv2.putText(frame, emocion,(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Detección de Caras', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
