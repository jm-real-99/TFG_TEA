import numpy as np
import cv2
from libraries.GazeTracking.gaze_tracking import GazeTracking


class GestorAtencion:
    def __init__(self):
        """*****************
        MODELOS DE DATOS
        ******************"""
        self._gaze = GazeTracking()

        """*****************
        VARIABLES DE DATOS
        ******************"""
        # Mediante esta variable controlaremos si el usuario está prestando atención actualmente. Lo usaremos para
        self._atencionActual = False
        # Mediante esta variable sabremos si en el segundo atencióin hubo atención. Gracias a ella cerraremos intervalos
        self._atencionPrevia = False
        # Mediante esta variable sabremos cuando hemos empezado a detectar el intervalo de la atención
        self._t_inicioAtencion = 0
        # Mediante esta variable sabremos el segundo en el que estamos. Esto nos permitirá saber si hemos cambiado la
        # atención en el mismo segundo.
        self._tiempoActual = 0
        # Array donde se almacenará una dupla (Ti,Tf) donde Ti es el segundo inicial del intervalo
        # dónde se ha prestado atención y Tf el final.
        self._intervalosAtencion = []
        # Array donde almacenaremos el tiempo total que se presta atención a lo largo de la
        # terapia, esto nos permitirá ahorrar tiempo de cómputo a la hora de calcular las estadísticas.
        self._tiempoTotalAtencion = 0

    """
     Detectamos la atención en el frame indicado
     :arg
            frame(cv2): Frame en el que nos encontramos
            tiempo (int): Segundo en que nos encontramos
        :return
            Boolean. Hay atención o no
            String. Lado donde miramos
    """
    def detectar_atencion(self, frame, face_dlib ,tiempo):
        self._gaze.refresh(frame,face_dlib)
        if self._gaze.is_center():
            text = "Centro"
            mirando = True
            self._atencionActual = True
        elif self._gaze.is_blinking():
            text = "Parpadeando"
            mirando = False
        elif self._gaze.is_right():
            text = "Mirando derecha"
            mirando = False
        elif self._gaze.is_left():
            text = "Mirando izquierda"
            mirando = False
        else:
            text = "Otro"
            mirando = False

        self.__evaluar_intervalo(tiempo)

        return mirando, text

    def __evaluar_intervalo(self, tiempo):

        # Si el tiempo recibido es mayor al actual procedemos a evaluar
        if self.__actualizar_tiempo(tiempo):
            # Si el tiempo anterior no teníamos atención y este hemos tenido atención entonces abrimos el intervalo
            if  not self._atencionPrevia and self._atencionActual:
                self._t_inicioAtencion = self._tiempoActual
            # Si el tiempo anterior teníamos atención y este no hemos tenido atención entonces cerramos el intervalo
            elif self._atencionPrevia and not self._atencionActual:
                self._intervalosAtencion.append((self._t_inicioAtencion, self._tiempoActual))
                self._tiempoTotalAtencion += (self._tiempoActual - self._t_inicioAtencion )
            # En el caso en el que no se cumpla ninguna de las dos es que o llevamos dos segundos seguidos sin cambios,
            # así que solo realizamos las actualizaciones de los segundos

            self._atencionPrevia = self._atencionActual
            self._atencionActual = False


    """
            Actualizamos el segundo si es que ya ha pasado el actual
            Args:
                tiempo(int): Tiempo actual
    """

    def __actualizar_tiempo(self, tiempo):
        if tiempo > self._tiempoActual:
            self._tiempoActual = tiempo
            return True
        return False

    """
        En el caso de que terminemos la ejecución y tengamos un intervalo abierto lo cerramos
        Args:
            tiempo(int): Tiempo actual
        """
    def terminar_escaneo(self,tiempo):
        if self._atencionActual:
            self._intervalosAtencion.append((self._t_inicioAtencion, tiempo))
            self._tiempoTotalAtencion += (tiempo - self._t_inicioAtencion) + 1

    """*****************************************
        ***********GETTERS AND SETTERS**************
        *****************************************"""

    def get_atencionactual(self):
        return self._atencionActual

    def get_intervalosatencion(self):
        return self._intervalosAtencion

    def get_tiempototalatencion(self):
        return self._tiempoTotalAtencion
