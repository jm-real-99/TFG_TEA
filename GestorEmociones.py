import dlib

from Emociones import Emociones
import numpy as np
import cv2
from deepface import DeepFace

from LoggerManager import LoggerManager


class GestorEmociones:
    """
    Clase donde vamos a realizar el análisis de las emociones
    """
    def __init__(self):

        # Inicializamos los logs:
        self._logger = LoggerManager.get_logger()

        """*****************
        VARIABLES DE DATOS
        ******************"""
        self._logger.info("[GESTOR EMOCIONES] Creamos las variables de datos")
        # Mediante esta variable controlaremos cuál es la emoción actual y sabremos si esta ha cambiado
        self._emocionActual = Emociones.NONE.value
        # Mediante esta variable sabremos cuando hemos empezado a detectar una emoción.
        self._t_inicioEmocion = 0
        # Mediante esta variable sabremos el segundo en el que estamos. Esto nos permitirá que si en el mismo segundo
        # detecta dos emociones distintas, entonces nos quedemos con la más importante.
        self._tiempo = 0
        # Diccionario clave-valor donde se almacenará una dupla (Ti,Tf) donde Ti es el segundo inicial del intervalo
        # dónde se ha mostrado la emoción y Tf el final. Esto se guardará en la emoción correspondiente.
        self._intervalosEmociones = {emotion.value: [] for emotion in Emociones}
        # Diccionario clave-valor donde almacenaremos el tiempo total quie se expresa la emoción a lo largo de la
        # terapia, esto nos permitirá ahorrar tiempo de cómputo a la hora de calcular las estadísticas.
        self._tiempoTotalEmocion = {emotion.value: 0 for emotion in Emociones}

        # Emociones suavizadas
        self._smoothEmotions = None
        self._logger.info("[GESTOR EMOCIONES] Variables de datos creadas")

    def detectar_emocion(self, frame, face , tiempo):
        """
        Realizamos el análisis del frame
        @param frame: Frame en el que nos encontramos
        @param face: Cara detectada
        @param tiempo: Segundo en el que nos encontramos
        @return: (EMOCIONES,Dict[str, float],(x, y, w, h ))
            - EMOCIONES: Enum de la emoción detectada
            - Dict[str, float]: Diccionario de las emociones analizadas con su probabilidad.
            - (x, y, w, h ): Coordenadas de la cara detectada y recortada
        """
        self._logger.info("[GESTOR EMOCIONES] Detectamos emoción")

        # Vemos si deberíamos de actualizar el tiempo actual
        self.__actualizar_tiempo(tiempo)

        if not face:
            self._logger.info("[GESTOR EMOCIONES] No se ha detectado cara")
            self.__cambiar_emocion(tiempo, Emociones.NONE.value)
            return self._emocionActual, None, None

        try:

            x, y, w, h = face

            face_crop = frame[y:y + h, x:x + w]
            # Analiza las emociones del rostro detectado

            analysis = DeepFace.analyze(face_crop, actions=['emotion'], detector_backend='skip',  enforce_detection=False)

            self._logger.info("[GESTOR EMOCIONES] Emociones analizadas")
            # Obtenemos el diccionario de las emociones detectadas junto a su %
            emotions = analysis[0]['emotion']

            # Suavizamos las emociones para que los cambios no sean tan bruscos
            self.suavizar_emociones(emotions)

            # Obtiene la emoción principal detectada
            dominant_emotion = max(self._smoothEmotions, key= self._smoothEmotions.get)

            self.__registrar_emocion(dominant_emotion, tiempo)

            self._logger.info("[GESTOR EMOCIONES] Análisis realizado")

            return self._emocionActual, self._smoothEmotions, face

        except Exception as e:
            self._logger.error(f"[GESTOR EMOCIONES] en detección de emoción: {e}")
            return self._emocionActual, None, None

    def suavizar_emociones(self, emotions, alpha=0.5):
        """
        Suavizado exponencial de las emociones, para evitar cambios bruscos
        @param emotions: Diccionario de las emociones con su probabilidad
        @param alpha: Suavizado de 0.5
        @return: None
        """
        self._logger.info("[GESTOR EMOCIONES] Suavizamos las emociones")
        if self._smoothEmotions is None:
            self._smoothEmotions = emotions
        else:
            self._smoothEmotions = {
                k: alpha * emotions[k] + (1 - alpha) * self._smoothEmotions[k]
                for k in emotions
            }
        self._logger.info("[GESTOR EMOCIONES] Emociones suavizadas")

    def __registrar_emocion(self, emocion, tiempo):
        """
        Función desde la que gestionamos la emoción actual detectada en el frame
        @param emocion: Emoción detectada del enum Emociones
        @param tiempo: Segundo actual
        @return:
        """
        self._logger.info("[GESTOR EMOCIONES] Registramos la emoción")
        # Para el caso de que el segundo actual sea el mismo, entonces solo cambiaremos de emocion si ha aparecido una
        # emocion distinta y esta no es prioritaria (no es NONE).
        if tiempo == self._tiempo and emocion != self._emocionActual and emocion != Emociones.NONE:
            self._logger.info("[GESTOR EMOCIONES] Emoción distinta detectada")
            self.__cambiar_emocion(tiempo, emocion)
        # Si hemos cambiado de tiempo y la emoción es distinta,entonces cambiamos la emocion actual
        if tiempo != self._tiempo and emocion != self._emocionActual:
            self.__cambiar_emocion(tiempo, emocion)
        # Para cualquier otro caso no hacemos nada.

    def __cambiar_emocion(self, tiempo, emocion):
        """
        Cambiamos de emoción detectada
        @param tiempo: Segundo actual
        @param emocion: Emoción detectada
        @return: None
        """
        self.__add_emotion_interval(tiempo)
        self._t_inicioEmocion = tiempo
        self._emocionActual = emocion

    def __add_emotion_interval(self, fin):
        """
        Agregamos un intervalo con la emoción que tenemos detectada actualmente
        @param fin: Segundo actual, en el que termina el intervalo
        @return: None
        """
        self._intervalosEmociones[self._emocionActual].append((self._t_inicioEmocion, fin))
        self._tiempoTotalEmocion[self._emocionActual] += (fin - self._t_inicioEmocion) + 1

    def __actualizar_tiempo(self, tiempo):
        """
        Actualizamos el segundo actual
        @param tiempo: Segundo actual
        @return: None
        """
        if tiempo > self._tiempo:
            self._tiempo = tiempo

    def terminar_escaneo(self, tiempo):
        """
        Terminamos el escaneo y si tenemos un intervalo abierto lo cerramos
        @param tiempo: Segundo actual y final
        @return: None
        """
        self.__add_emotion_interval(tiempo)

    """*****************************************
    ***********GETTERS AND SETTERS**************
    *****************************************"""

    def get_emocionactual(self):
        return self._emocionActual

    def get_intervalosemociones(self):
        return self._intervalosEmociones

    def get_tiempototalemocion(self):
        return self._tiempoTotalEmocion

    def get_smoothemotions(self):
        return self._smoothEmotions