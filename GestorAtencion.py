import numpy as np
import cv2

from LoggerManager import LoggerManager
from libraries.GazeTracking.gaze_tracking import GazeTracking


class GestorAtencion:
    """
    Clase donde gestionamos el análisis de la atención a lo largo de la terapia.
    """
    def __init__(self):

        # Inicializamos los logs:
        self._logger = LoggerManager.get_logger()

        """
        MODELOS DE DATOS
        """
        self._logger.info("[GESTOR ATENCIÓN] Creamos entidad GazeTracking")
        # Creamos la entidad de GazeTracking para hacer el análisis
        self._gaze = GazeTracking()
        self._logger.info("[GESTOR ATENCIÓN] Entidad GazeTracking creada con éxito")

        """
        VARIABLES DE DATOS
        """
        self._logger.info("[GESTOR ATENCIÓN] Creamos las variables de datos")
        # Mediante esta variable controlaremos si el usuario está prestando atención actualmente.
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
        self._logger.info("[GESTOR ATENCIÓN] Variables de datos creadas con éxito")

    def detectar_atencion(self, frame, face_dlib ,tiempo):
        """
        Detectamos la atención en el frame indicado
        @param frame: Frame a analizar
        @param face_dlib: Cara detectada
        @param tiempo: Segundo en el que nos encontramos
        @return: (Boolean, String)
            - Boolean:
                - True si el paciente está prestando atención
                - False si el paciente no está prestando atención
            - String: Texto de hacia dónde está mirando el paciente.
        """
        self._logger.info("[GESTOR ATENCIÓN] Detectamos la atención")
        self._gaze.refresh(frame,face_dlib)
        if self._gaze.is_center():
            self._logger.info("[GESTOR ATENCIÓN] El usuario está mirando al centro")
            text = "Centro"
            mirando = True
            self._atencionActual = True
        elif self._gaze.is_blinking():
            self._logger.info("[GESTOR ATENCIÓN] El usuario está parpadeando")
            text = "Parpadeando"
            mirando = False
        elif self._gaze.is_right():
            self._logger.info("[GESTOR ATENCIÓN] El usuario está mirando a la derecha")
            text = "Mirando derecha"
            mirando = False
        elif self._gaze.is_left():
            self._logger.info("[GESTOR ATENCIÓN] El usuario está mirando a la izquierda")
            text = "Mirando izquierda"
            mirando = False
        else:
            self._logger.info("[GESTOR ATENCIÓN] No se ha detectado atención")
            text = "Otro"
            mirando = False

        self.__evaluar_intervalo(tiempo)

        self._logger.info("[GESTOR ATENCIÓN] Analisis finalizando")
        return mirando, text

    def __evaluar_intervalo(self, tiempo):
        """
        Evaluamos si cambiamos de segundo y la acción a realizar con el intervalo
        @param tiempo: Segundo en el que nos encontramos
        @return: None
        """
        self._logger.info("[GESTOR ATENCIÓN] Evaluamos el intervalo")
        # Si el tiempo recibido es mayor al actual procedemos a evaluar
        if self.__actualizar_tiempo(tiempo):
            # Si el tiempo anterior no teníamos atención y este hemos tenido atención entonces abrimos el intervalo
            if  not self._atencionPrevia and self._atencionActual:
                self._logger.info("[GESTOR ATENCIÓN] Abrimos intervalo")
                self._t_inicioAtencion = self._tiempoActual
            # Si el tiempo anterior teníamos atención y este no hemos tenido atención entonces cerramos el intervalo
            elif self._atencionPrevia and not self._atencionActual:
                self._logger.info("[GESTOR ATENCIÓN] Cerramos intervalo")
                self._intervalosAtencion.append((self._t_inicioAtencion, self._tiempoActual-1))
                self._tiempoTotalAtencion += (self._tiempoActual - self._t_inicioAtencion )
            # En el caso en el que no se cumpla ninguna de las dos es que o llevamos dos segundos seguidos sin cambios,
            # así que solo realizamos las actualizaciones de los segundos

            self._atencionPrevia = self._atencionActual
            self._atencionActual = False
            self._logger.info("[GESTOR ATENCIÓN] Cambiamos de segundo")
        self._logger.info("[GESTOR ATENCIÓN] Intervalo analizado")

    def __actualizar_tiempo(self, tiempo):
        """
        Actualizamos el segundo si es que ya ha pasado el actual
        @param tiempo:
        @return: Boolean
            - True si hemos pasado de segundo
            - False si continuamos en el mismo segundo
        """
        if tiempo > self._tiempoActual:
            self._logger.info("[GESTOR ATENCIÓN] Actualizamos el tiempo")
            self._tiempoActual = tiempo
            return True
        return False

    def terminar_escaneo(self,tiempo):
        """
        Terminamos el análisis y si tenemos un intervalo abierto lo cerramos.
        @param tiempo: Segundo actual
        @return: None
        """
        self._logger.info("[GESTOR ATENCIÓN] Terminamos el escaneo")
        if self._atencionActual:
            self._intervalosAtencion.append((self._t_inicioAtencion, tiempo))
            self._tiempoTotalAtencion += (tiempo - self._t_inicioAtencion) + 1

    """*********************************************
        ***********GETTERS AND SETTERS**************
        ********************************************"""

    def get_atencionactual(self):
        return self._atencionActual

    def get_intervalosatencion(self):
        return self._intervalosAtencion

    def get_tiempototalatencion(self):
        return self._tiempoTotalAtencion
