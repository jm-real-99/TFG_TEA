from Emociones import Emociones
import numpy as np
import cv2
import dlib
from tensorflow import keras

class GestorEmociones:
    def __init__(self):
        """*****************
        MODELOS DE DATOS
        ******************"""
        # Cargar el modelo pre-entrenado de detección de caras de OpenCV
        self._face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self._predictor = dlib.shape_predictor("modelos/shape_predictor_68_face_landmarks.dat")
        # Cargamos el modelo preentrenado, ver la referencia para saber de dónde lo he sacado
        # (quizás tenga que entrenar yo mismo uno)
        self._model = keras.models.load_model("modelos/model.h5")
        # Inicializamos la cámara web

        """*****************
        VARIABLES DE DATOS
        ******************"""
        # Mediante esta variable controlaremos cuál es la emoción actual y sabremos si esta ha cambiado
        self._emocionActual = Emociones.NEUTRO
        # Mediante esta variable sabremos cuando hemos empezado a detectar una emoción.
        self._t_inicioEmocion = 0
        # Mediante esta variable sabremos el segundo en el que estamos. Esto nos permitirá que si en el mismo segundo
        # detecta dos emociones distintas, entonces nos quedemos con la más importante.
        self._tiempo = 0
        # Diccionario clave-valor donde se almacenará una dupla (Ti,Tf) donde Ti es el segundo inicial del intervalo
        # dónde se ha mostrado la emoción y Tf el final. Esto se guardará en la emoción correspondiente.
        self._intervalosEmociones = {emotion: [] for emotion in Emociones}
        # Diccionario clave-valor donde almacenaremos el tiempo total quie se expresa la emoción a lo largo de la
        # terapia, esto nos permitirá ahorrar tiempo de cómputo a la hora de calcular las estadísticas.
        self._tiempoTotalEmocion = {emotion: [] for emotion in Emociones}

    """
        Detectamos las emociones en el frame indicado
        :arg
            frame(cv2): Frame en el que nos encontramos
            tiempo (int): Segundo en que nos encontramos
        :return
            String. Emocion
    """

    def detectar_emocion(self,frame,tiempo):
        print("Entramos en detectar_emocion")
        # Vemos si deberíamos de actualizar el tiempo actual
        self.__actualizar_tiempo(tiempo)

        # Detectamos caras en el fotograma
        faces = self._face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            # Dibujamos un rectángulo alrededor de la cara detectada
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Obtenemos los puntos de referencia faciales
            landmarks = self._predictor(frame, dlib.rectangle(x, y, x + w, y + h))

            # Dibujamos los puntos recogidos en landmarks
            for i in range(68):  # 68 puntos de referencia faciales
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Extraemos la región de interés (ROI) y la redimensionamos
            roi = frame[y:y + h, x:x + w]
            resized = cv2.resize(roi, (48, 48))

            # Realizamos la predicción utilizando el modelo cargado
            prediction = self._model.predict(np.array([resized]).reshape(1, 48, 48, 1))[0]

            # Del vector con las probabilidades de emociones, cogemos el más probable.
            print(prediction)
            print(np.argmax(prediction))
            emocionmax = list(Emociones)[np.argmax(prediction)]
            print(emocionmax)
            print(emocionmax.name)
            self.__registrar_emocion(emocionmax,tiempo)
            print("Vamos a devolver: "+self._emocionActual.name)
            return self._emocionActual

    """
        Funcion desde la que gestionamos la emoción actual del frame
        Args:
            tiempo (int): Tiempo actual
            emocion (int): Emoción detectada del enum Emociones
        """
    def __registrar_emocion(self,emocion,tiempo):
        # Para el caso de que el segundo actual sea el mismo, entonces solo cambiaremos de emocion si ha aparecido una
        # emocion distinta y esta no es prioritaria (no es NEUTRO).
        if tiempo == self._tiempo and emocion != self._emocionActual and emocion != Emociones.NEUTRO:
            self.__cambiar_emocion(tiempo, emocion)
        # Si hemos cambiado de tiempo y la emoción es distinta,entonces cambiamos la emocion actual
        if tiempo != self._tiempo and emocion != self._emocionActual:
            self.__cambiar_emocion(tiempo, emocion)
        # Si no hemos cambiado de tiempo, pero la emoción es la misma, le sumamos un segundo a la emoción actual
        elif tiempo != self._tiempo and emocion != self._emocionActual:
            self._tiempoTotalEmocion[emocion] += 1
        #Para cualquier otro caso no hacemos nada.

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
    def __add_emotion_interval(self,fin):
        print("Añadimos emocion "+self._emocionActual.name+": ("+str(self._t_inicioEmocion)+","+str(fin)+")")
        self._intervalosEmociones[self._emocionActual].append((self._t_inicioEmocion, fin))

    """
        Actualizamos el segundo si es que ya ha pasado el actual
        Args:
            tiempo(int): Tiempo actual
    """
    def __actualizar_tiempo(self, tiempo):
        if tiempo > self._tiempo:
            self._tiempo = tiempo

    """
        Hemos terminado la terapia así que exportaremos los datos de recabados a la base de datos
    """
    def exportar_datos(self):
        #TODO: implementar funcionalidad
        pass

    """
        Obtenemos la emoción actual
        Return: Emocion
    """
    def get_emocionactual(self):
        return self._emocionActual
