from Emociones import Emociones
import numpy as np
import cv2
from deepface import DeepFace

class GestorEmociones:
    def __init__(self):
        """*****************
        VARIABLES DE RECONOCIMIENTO FACIAL
        ******************"""
        # Inicializamos el clasificador en cascada de Haar para detección facial
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            raise RuntimeError("Error: No se pudo cargar el clasificador en cascada de Haar")
        """*****************
        VARIABLES DE DATOS
        ******************"""
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

        self._smoothEmotions = None

    """
        Detectamos las emociones en el frame indicado
        :arg
            frame(cv2): Frame en el que nos encontramos
            tiempo (int): Segundo en que nos encontramos
        :return
            String. Emocion
    """

    def detectar_emocion(self, frame, tiempo):

        # Vemos si deberíamos de actualizar el tiempo actual
        self.__actualizar_tiempo(tiempo)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) <= 0:
            self.__cambiar_emocion(tiempo, Emociones.NONE.value)
            return self._emocionActual, None, None

        try:
            x, y, w, h = faces[0]
            face_crop = frame[y:y + h, x:x + w]
            # Analiza las emociones del rostro detectado
            analysis = DeepFace.analyze(face_crop, actions=['emotion'], detector_backend='skip',  enforce_detection=False)


            # Obtenemos el diccionario de las emociones detectadas junto a su %
            emotions = analysis[0]['emotion']

            # Suavizamos las emociones para que los cambios no sean tan bruscos
            self.suavizar_emociones(emotions)

            # Obtiene la emoción principal detectada
            dominant_emotion = max(self._smoothEmotions, key= self._smoothEmotions.get)
            # dominant_emotion = analysis[0]['dominant_emotion']

            self.__registrar_emocion(dominant_emotion, tiempo)

            return self._emocionActual, self._smoothEmotions, faces[0]

        except Exception as e:
            print(f"[ERROR] en detección de emoción: {e}")
            return self._emocionActual, None, None

    """
     Suaviazado exponencial con factor alpha a 0.5
    """

    def suavizar_emociones(self, emotions, alpha=0.5):
        if self._smoothEmotions is None:
            self._smoothEmotions = emotions
        else:
            self._smoothEmotions = {
                k: alpha * emotions[k] + (1 - alpha) * self._smoothEmotions[k]
                for k in emotions
            }

    """
        Funcion desde la que gestionamos la emoción actual del frame
        Args:
            tiempo (int): Tiempo actual
            emocion (int): Emoción detectada del enum Emociones
        """

    def __registrar_emocion(self, emocion, tiempo):
        # Para el caso de que el segundo actual sea el mismo, entonces solo cambiaremos de emocion si ha aparecido una
        # emocion distinta y esta no es prioritaria (no es NONE).
        if tiempo == self._tiempo and emocion != self._emocionActual and emocion != Emociones.NONE:
            self.__cambiar_emocion(tiempo, emocion)
        # Si hemos cambiado de tiempo y la emoción es distinta,entonces cambiamos la emocion actual
        if tiempo != self._tiempo and emocion != self._emocionActual:
            self.__cambiar_emocion(tiempo, emocion)
        # Para cualquier otro caso no hacemos nada.

    """
            Actualizamos las variables actuales referidas a la emocion actual
            Args:
                tiempo (int): Tiempo actual
                emocion (int): Emoción detectada del enum Emociones
        """

    def __cambiar_emocion(self, tiempo, emocion):
        self.__add_emotion_interval(tiempo)
        self._t_inicioEmocion = tiempo
        self._emocionActual = emocion

    """
        Agregamos un intervalo con la emoción específica
        Args:
            comienzo (int): Tiempo de inicio en segundos.
            fin (int): Tiempo de fin en segundos.
            emocion (int): Emoción detectada del enum Emociones
    """

    def __add_emotion_interval(self, fin):
        self._intervalosEmociones[self._emocionActual].append((self._t_inicioEmocion, fin))
        self._tiempoTotalEmocion[self._emocionActual] += (fin - self._t_inicioEmocion) + 1

    """
        Actualizamos el segundo si es que ya ha pasado el actual
        Args:
            tiempo(int): Tiempo actual
    """

    def __actualizar_tiempo(self, tiempo):
        if tiempo > self._tiempo:
            self._tiempo = tiempo

    """
            En el caso de que terminemos la ejecución y tengamos un intervalo abierto lo cerramos
            Args:
                tiempo(int): Tiempo actual
            """

    def terminar_escaneo(self, tiempo):
        self.__add_emotion_interval(tiempo)

    """
        Hemos terminado la terapia así que exportaremos los datos de recabados a la base de datos
    """

    def exportar_datos(self):
        # TODO: implementar funcionalidad
        pass

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