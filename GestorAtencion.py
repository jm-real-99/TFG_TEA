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
        # Si estamos mirando al centro y en el segundo anterior no teniamos la atención entonces iniciamos intervalo
        if self._gaze.is_center() and not self._atencionActual:
            self._atencionActual = True
            self._t_inicioAtencion = tiempo
            self.__actualizar_tiempo(tiempo)
            return True, "Centro"
        # Si estamos mirando al centro y en el anterior también entonces sumamos uno a la cuenta del intervalo
        elif self._gaze.is_center() and tiempo > self._tiempoActual and self._atencionActual:
            self._atencionActual = True
            self.__actualizar_tiempo(tiempo)
            return True, "Centro"
        # Si no estamos mirando al centro, durante el segundo anterior no lo hemos hecho y lo tenemos marcado como visto
        # , entonces terminamos el intervalo en el anterior segundo
        elif (not self._gaze.is_center()) and tiempo > self._tiempoActual + 1 and self._atencionActual:
            self._intervalosAtencion.append((self._t_inicioAtencion, self._tiempoActual))
            self._tiempoTotalAtencion += (self._tiempoActual - self._t_inicioAtencion) + 1
            self._atencionActual = False

        if self._gaze.is_blinking():
            text = "Blinking"
        elif self._gaze.is_right():
            text = "Looking right"
        elif self._gaze.is_left():
            text = "Looking left"
        else:
            return True, "Centro"
        return False, text

    """
            Actualizamos el segundo si es que ya ha pasado el actual
            Args:
                tiempo(int): Tiempo actual
    """

    def __actualizar_tiempo(self, tiempo):
        if tiempo > self._tiempoActual:
            self._tiempoActual = tiempo

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
