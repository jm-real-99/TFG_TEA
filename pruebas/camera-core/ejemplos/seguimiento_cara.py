# Autor: Juan Manuel Real Domínguez

# Este ha sido el primer script desarrollado, ya que es la base del resto. Aquí lo que hacemos es detectar y seguir la
# cara de una persona mediante la webcam.
# Para ello dibujaremos un cuadraro al rededor de la cara.

import cv2

# Cargamos el modelo pre-entrenado de detección de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializamos la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturamos un fotograma de la cámara
    ret, frame = cap.read()

    # Convertimos el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectamos las caras en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Dibujamos un rectángulo alrededor de cada cara detectada
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostramos el fotograma con las caras detectadas
    cv2.imshow('Detección de Caras', frame)

    # Salimos del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finalmente, liberamos la cámara y cerramos la ventana
cap.release()
cv2.destroyAllWindows()
