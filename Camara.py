import cv2
import dlib

from LoggerManager import LoggerManager

from Emociones import Emociones
import numpy as np
import time
from datetime import datetime

from GestorAtencion import GestorAtencion
from GestorEmociones import GestorEmociones
from Estadistica import Estadistica
from concurrent.futures import ThreadPoolExecutor


class Camara:
    """
    Creamos y gestionamos la cámara durante las terpias.
    """
    def __init__(self, camera, estadistica):
        # Inicializamos los logs:
        self._logger = LoggerManager.get_logger()

        self._cap = cv2.VideoCapture(camera)
        self._tiempoInicio = time.time()
        self._gestorEmociones = GestorEmociones()
        self._gestorAtencion = GestorAtencion()
        self._estadisticas = estadistica

        self.fps = 0
        self.lastSecond = 0


        self._face_detector =  dlib.get_frontal_face_detector()
        self._face_dlib = None
        self._face = None
        self._ultimo_segundo_cara = 0

        # self._executor = ProcessPoolExecutor(max_workers=2)
        self._executor = ThreadPoolExecutor(max_workers=2)

    def read_frame(self):
        """
        Leemos el frame de la cámara.
        @return: Devolvemos un Boolean.
            True si continuamos con la lectura
            False si no continuamos con la lectura, es decir, hemos detectado una interrupción
        """
        ret, frame = self._cap.read()

        segundo_actual =  self.__segundo_actual()

        if not ret:
            print("[DETECTAR EMOCION]Terminamoos")
            return

        self.__detectar_cara(frame)

        # Valores por defecto para mostrar. Serán si hay fallo
        texto_emocion = "No se detecta la cara"
        color_emocion = (0, 0, 255)
        color_atencion = (0, 0, 255)
        text_atencion = "No se detecta la cara"
        emociones = None

        # Solo hacemos la evaluación si se ha detectado un cara
        if self._face:

            try:
                emocion, emociones, face = self._gestorEmociones.detectar_emocion(frame, self._face , segundo_actual)
            except Exception as e:
                self._logger.error(f"Error al detectar emoción: {e}")
                emocion, emociones, face = None, {}, None

            try:
                atencion, text_atencion = self._gestorAtencion.detectar_atencion( frame, self._face_dlib, segundo_actual)
            except Exception as e:
                self._logger.error(f"Error al detectar atención: {e}")
                atencion, text_atencion = False, "Atención desconocida"

            # Agregamos el texto a la imagen
            if emocion is not None:
                texto_emocion = emocion
                color_emocion = (0, 255, 0)

            if atencion:
                color_atencion = (0, 255, 0)

        cv2.putText(frame, texto_emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_emocion, 2)
        cv2.putText(frame, text_atencion, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color_atencion, 2)
        cv2.putText(frame, str(self.__segundo_actual()), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if self._face is not None:
            x,y,w,h = self._face
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)

        # Terminamos el proceso si se ha interrumpido
        if self.__terminar_proceso():
            return False
        else:
            return True, frame, emociones

    def __detectar_cara(self, frame):
        """
        Detectamos la cara en el frame. Además realizamos una aproximación a la cara principal en caso de que se
        detecten varias.
        @param frame: Frame a analizar
        @return: None
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_dlib = self._face_detector(gray)

        # Reiniciar si han pasado más de 2 segundos sin cara
        segundo_actual = self.__segundo_actual()
        if hasattr(self, '_ultimo_segundo_cara') and segundo_actual - self._ultimo_segundo_cara > 2:
            self._face = None
            self._face_dlib = None

        if not faces_dlib:
            return None  # No se detectó cara

        mejor = None
        i = -1
        # Si hay una cara anterior, buscamos la más cercana
        if hasattr(self, '_face') and self._face is not None:
            i+=1
            x_prev, y_prev, w_prev, h_prev = self._face
            centro_prev = np.array([x_prev + w_prev / 2, y_prev + h_prev / 2])

            menor_distancia = float('inf')
            for rect in faces_dlib:
                x = rect.left()
                y = rect.top()
                w = rect.width()
                h = rect.height()
                centro = np.array([x + w / 2, y + h / 2])
                distancia = np.linalg.norm(centro - centro_prev)

                if distancia < menor_distancia:
                    menor_distancia = distancia
                    mejor = (x, y, w, h)
        else:
            # Si no hay cara previa, tomamos la primera
            rect = faces_dlib[0]
            i = 0
            mejor = (rect.left(), rect.top(), rect.width(), rect.height())

        # Guardamos la última cara y el segundo en que fue vista
        self._face = mejor
        self._face_dlib = faces_dlib[i]
        self._ultimo_segundo_cara = segundo_actual

    def __segundo_actual(self):
        """
        Calculamos el tiempo que lleva la cámara encendida y por tanto, de terapia.
        @return: Int
        """
        return int(time.time() - self._tiempoInicio)

    def cerrar_camara(self):
        """
        La terapia ha finalizado, por lo que cerramos la cámara y recabamos las estadísticas de los módulos.
        @return:
        """
        self._cap.release()
        cv2.destroyAllWindows()

        self._gestorAtencion.terminar_escaneo(self.__segundo_actual())
        self._gestorEmociones.terminar_escaneo(self.__segundo_actual())

        self.__recabar_estadisticas()

    def __recabar_estadisticas(self):
        """
        Cargamos en estadísticas los datos recabados durante la terapia.
        @return: None
        """
        self._estadisticas.set_tiempototal(self.__segundo_actual())
        self._estadisticas.set_horafin(datetime.now())
        total_emociones = self._gestorEmociones.get_tiempototalemocion()
        self._estadisticas.convertir_JSON_emociones(self._gestorEmociones.get_intervalosemociones())
        self._estadisticas.set_enfadadototal(total_emociones[Emociones.ENFADO.value])
        self._estadisticas.set_disgustadototal(total_emociones[Emociones.DISGUSTADO.value])
        self._estadisticas.set_miedosototal(total_emociones[Emociones.MIEDOSO.value])
        self._estadisticas.set_contentototal(total_emociones[Emociones.CONTENTO.value])
        self._estadisticas.set_tristetotal(total_emociones[Emociones.TRISTE.value])
        self._estadisticas.set_sorprendidototal(total_emociones[Emociones.SORPRENDIDO.value])
        self._estadisticas.set_neutrototal(total_emociones[Emociones.NEUTRO.value])
        self._estadisticas.convertir_JSON_cambios(self._gestorEmociones.get_cambiosbruscos())
        self._estadisticas.convertir_JSON_atencion(self._gestorAtencion.get_intervalosatencion())
        self._estadisticas.set_atenciontotal(self._gestorAtencion.get_tiempototalatencion())

    def __terminar_proceso(self):
        """
        Evaluamos si el usuario ha terminado el proceso
        @return: Booleano
            True si se ha terminado
            False si no
        """
        return cv2.waitKey(1) & 0xFF == ord('q')
