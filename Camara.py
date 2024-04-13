import cv2
from Emociones import Emociones
import numpy as np
import time
import GestorEmociones


class Camara:
    def __init__(self, camera):
        self._cap = cv2.VideoCapture(camera)
        self._tiempoInicio = time.time()
        self._gestorEmociones = GestorEmociones()

    """
        Leemos el frame de la cámara.
        Return: boolean
            True si continuamos con la lectura
            False si no continuamos con la lectura, es decir, hemos detectado una interrupción
    """
    def read_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # LLAMAMOS A LA CLASE DE GESTOR EMOCIONES
        # TODO: Llamar mediante un hilo aparte
        emocion = self.gestorEmociones.detectar_emocion(gray, self.segundo_actual())

        # LLAMAMOS A LA CLASE DE GESTOR EMOCIONES
        # TODO: Llamar mediante un hilo aparte
        
        # TODO: Incluir un semaforo que controle que ambas cosas se han hecho
        # Agregamos el texto a la imagen
        cv2.putText(frame, emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Detección de Caras', frame)

        #Terminamos el proceso si se ha interrumpido
        if self.terminar_proceso():
            self.cap.release()
            cv2.destroyAllWindows()
            return False
        else:
            return True

    """"
        Calculamos el tiempo que lleva la cámara encendida.
            return: int
                
    """
    def __segundo_actual(self):
        return int(time.time() - self.tiempoInicio)

    """
        Evaluamos si el usuario ha terminado el proceso
        Return: boolean
            True si se ha terminado
            False si no
    """
    def __terminar_proceso(self):
        return cv2.waitKey(1) & 0xFF == ord('q')
