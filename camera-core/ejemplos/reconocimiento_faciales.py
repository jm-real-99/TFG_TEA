# Autor: Juan Manuel Real Domínguez

# Este es un script que hice de ejemplo para comprobar si se podía y con qué eficacia se podría trackear puntos en la
# cara usando la librería dlib. Se tomó como punto de partida el script seguimiento_cara.py y se amplió usando
# como referencia el script que se incluye en la librería dlib (http://dlib.net/) face_landmark_detection.py

import cv2
import dlib

# Cargamos el modelo pre-entrenado de detección de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")

# Inicializamos la cámara web
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectamos las caras en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Dibujamos un rectángulo alrededor de la cara detectada
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Obtenemos los puntos de referencia faciales
        landmarks = predictor(gray, dlib.rectangle(x, y, x+w, y+h))

        # Dibujamos los puntos recogidos en landmarks
        for i in range(68):  # Tenemos hasta 68 puntos de referencia faciales
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow('Detección de Caras', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
