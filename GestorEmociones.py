from Emociones import Emociones
import numpy as np
import cv2
from deepface import DeepFace

# TODO: CAMBIAR LA IMPLEMENTACIÓN DE LECTURA DE EMOCIONES PARA USAR DeepFace

class GestorEmociones:
    def __init__(self):
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

    """
        Detectamos las emociones en el frame indicado
        :arg
            frame(cv2): Frame en el que nos encontramos
            tiempo (int): Segundo en que nos encontramos
        :return
            String. Emocion
    """

    def detectar_emocion(self, frame, tiempo):
        print("Entramos en detectar_emocion")
        # Vemos si deberíamos de actualizar el tiempo actual
        print("[DETECTAR EMOCION] Actualizamos tiempo")
        self.__actualizar_tiempo(tiempo)

        # Detectamos caras en el fotograma
        print("[DETECTAR EMOCION] Detectamos cara")
        faces = DeepFace.extract_faces(frame, detector_backend='opencv', enforce_detection=False)
        print("[DETECTAR EMOCION] Ya tenemos faces")
        print(faces)
        #TODO: ¿Qué hacemos si detecta más de una cara?
        if faces:
            try:
                face = faces[0]
                # Obtiene las coordenadas del área facial detectada
                facial_area = face['facial_area']
                x = facial_area['x']
                y = facial_area['y']
                w = facial_area['w']
                h = facial_area['h']

                # Analiza las emociones del rostro detectado
                print("[DETECTAR EMOCION]Analizamos emocion")
                analysis = DeepFace.analyze(frame[y:y + h, x:x + w], actions=['emotion'], enforce_detection=False)

                # Obtiene la emoción principal detectada
                print("[DETECTAR EMOCION]Obtenemos emocion dominante")
                dominant_emotion = analysis[0]['dominant_emotion']

                print("--Dominant emotion:")
                print(dominant_emotion)

                self.__registrar_emocion(dominant_emotion, tiempo)

                print("\t\t\t\tVamos a devolver: " + self._emocionActual)
                return self._emocionActual
            except FileNotFoundError:
                print("ERROR: El archivo no se encontró")
                input("Presione cualquier tecla para continuar")
                return self._emocionActual
            except ValueError as e:
                print(f"[ADVERTENCIA] No se detectó ningún rostro: {e}")
                return self._emocionActual
        else:
            #Si no detectamos una cara entonces marcamos vacío
            self.__cambiar_emocion(Emociones.NONE.value, tiempo)

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
        print(
            "Añadimos emocion " + self._emocionActual + ": (" + str(self._t_inicioEmocion) + "," + str(fin) + ")")
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
