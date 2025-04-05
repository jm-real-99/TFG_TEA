import cv2
from deepface import DeepFace

# Inicializa la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Detecta rostros en el fotograma
    faces = DeepFace.extract_faces(frame, detector_backend='opencv')

    for face in faces:
        # Obtiene las coordenadas del rostro detectado
        # x, y, w, h = face['facial_area'].values()
        x = face['facial_area']['x']
        y = face['facial_area']['y']
        w = face['facial_area']['w']
        h = face['facial_area']['h']

        # Analiza las emociones del rostro detectado
        analysis = DeepFace.analyze(frame[y:y+h, x:x+w], actions=['emotion'], enforce_detection=False)

        # Obtiene la emoción principal detectada
        dominant_emotion = analysis[0]['dominant_emotion']

        # Dibuja un rectángulo alrededor del rostro y muestra la emoción detectada
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, dominant_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Muestra el fotograma con las detecciones
    cv2.imshow('Detección de Emociones', frame)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura de video y cierra las ventanas
cap.release()
cv2.destroyAllWindows()


