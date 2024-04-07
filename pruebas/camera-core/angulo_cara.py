import cv2
import dlib
import numpy as np

# Cargar el modelo preentrenado de puntos de referencia faciales
predictor_path = "modelos/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Inicializar el detector de caras de dlib
detector = dlib.get_frontal_face_detector()

# Inicializamos la cámara web
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en el fotograma
    faces = detector(gray)

    for face in faces:
        # Obtener puntos de referencia faciales
        landmarks = predictor(gray, face)

        # Convertir los puntos de referencia a un array de numpy
        landmarks_np = np.array([[p.x, p.y] for p in landmarks.parts()])

        # Obtener los puntos extremos de los ojos (puedes ajustar estos índices según los landmarks específicos que desees usar)
        left_eye = landmarks_np[36]  # Punto 36: esquina izquierda del ojo izquierdo
        right_eye = landmarks_np[45]  # Punto 45: esquina derecha del ojo derecho

        # Dibujar los puntos en la imagen
        cv2.circle(frame, tuple(left_eye), 2, (0, 0, 255), -1)  # Pinta un círculo en la punta de la nariz
        cv2.circle(frame, tuple(right_eye), 2, (0, 0, 255), -1)  # Pinta un círculo en el centro del labio superior

        # Calcular el ángulo de giro del cuello (lateral)
        angle1 = np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]) * 180.0 / np.pi

        # Obtener puntos de referencia para la barbilla y las orejas (ajusta estos índices según los landmarks específicos que desees usar)
        left_ear = landmarks_np[2]  # Punto 2: oreja izquierda
        right_ear = landmarks_np[14]  # Punto 14: oreja derecha

        cv2.circle(frame, tuple(left_ear), 2, (0, 255, 0), -1)  # Pinta un círculo en la punta de la nariz
        cv2.circle(frame, tuple(right_ear), 2, (0, 255, 0), -1)  # Pinta un círculo en la punta de la nariz

        # Calcular el punto medio entre las orejas
        ear_midpoint = (left_ear + right_ear) // 2
        # Calcular el punto medio entre los ojos
        eye_midpoint = (left_eye + right_eye) // 2

        cv2.circle(frame, tuple(ear_midpoint), 2, (255, 255, 0), -1)  # Pinta un círculo en la punta de la nariz
        cv2.circle(frame, tuple(eye_midpoint), 2, (255, 255, 0), -1)  # Pinta un círculo en la punta de la nariz

        # Calcular la distancia entre los puntos medios
        distance_between_midpoints = np.linalg.norm(ear_midpoint - eye_midpoint)

        print(f"Ángulo horizontal cabeza: {angle1} \t Angulo vertical cabeza: {distance_between_midpoints}")
        if (-4 < angle1 < 4) and (102 < distance_between_midpoints < 119):
            print("\nCENTRO\n")

    cv2.imshow('Detección de Caras', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
