import cv2
import dlib
import tkinter as tk
from PIL import Image, ImageTk

# Cargamos el modelo pre-entrenado de detección de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")

# Inicializamos la cámara web
cap = cv2.VideoCapture(2)  # Cambia el índice a 0 o 1 según tu cámara

# Función para actualizar los fotogramas en el Canvas
def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        landmarks = predictor(gray, dlib.rectangle(x, y, x+w, y+h))
        for i in range(68):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Convertimos el fotograma de OpenCV a un formato que Tkinter pueda mostrar
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, update_frame)

# Función para detener la cámara
def detener_camara():
    cap.release()
    root.quit()

# Crear ventana Tkinter
root = tk.Tk()
root.title("Webcam App")

# Crear un label para mostrar la imagen de la cámara
lmain = tk.Label(root)
lmain.pack()

# Crear botón para detener la cámara
btn_detener = tk.Button(root, text="Detener Cámara", command=detener_camara)
btn_detener.pack()

# Iniciar la actualización de los fotogramas
update_frame()

root.mainloop()