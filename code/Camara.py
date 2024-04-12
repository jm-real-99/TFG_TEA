import cv2
from Emociones import Emociones
import numpy as np
import time
import GestorEmociones


class Camara:
    def __init__(self, camera):
        self.cap = cv2.VideoCapture(camera)
        self.tiempoInicio = time.time()
        self.gestorEmociones = GestorEmociones()

    def readFrame(self):
        ret, frame = self.cap.read()

        if not ret:
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # LLAMAMOS A LA CLASE DE GESTOR EMOCIONES
        # TODO: Llamar mediante un hilo aparte
        emocion = self.gestorEmociones.detectar_emocion(frame, self.segundo_actual())

        # LLAMAMOS A LA CLASE DE GESTOR EMOCIONES
        # TODO: Llamar mediante un hilo aparte
        
        # TODO: Incluir un semaforo que controle que ambas cosas se han hecho
        # Agregamos el texto a la imagen
        cv2.putText(frame, emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Detección de Caras', frame)

    """"
    Calculamos el tiempo que lleva la cámara encendida.
        return: Int.
    """

    def segundo_actual(self):
        return int(time.time() - self.tiempoInicio)
