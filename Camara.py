import cv2
from Emociones import Emociones
import numpy as np
import time
from datetime import datetime

from GestorAtencion import GestorAtencion
from GestorEmociones import GestorEmociones
from Estadistica import Estadistica
from concurrent.futures import ThreadPoolExecutor


class Camara:
    def __init__(self, camera, estadistica):
        self._cap = cv2.VideoCapture(camera)
        self._tiempoInicio = time.time()
        self._gestorEmociones = GestorEmociones()
        self._gestorAtencion = GestorAtencion()
        self._estadisticas = estadistica

        self._executor = ThreadPoolExecutor(max_workers=2)
    """
        Leemos el frame de la cámara.
        Return: boolean
            True si continuamos con la lectura
            False si no continuamos con la lectura, es decir, hemos detectado una interrupción
    """

    def read_frame(self):
        print("[CAMARA]Leemos frame")
        ret, frame = self._cap.read()

        if not ret:
            print("[DETECTAR EMOCION]Terminamoos")
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Lanzar tareas en paralelo
        print("Detectamos emocion")
        future_emocion = self._executor.submit(
            self._gestorEmociones.detectar_emocion, frame, self.__segundo_actual()
        )
        print("Detectamos atencion")
        future_atencion = self._executor.submit(
            self._gestorAtencion.detectar_atencion, frame, self.__segundo_actual()
        )

        # Esperamos a que terminen y obtenemos los resultados recabados
        emocion = future_emocion.result()
        atencion, text_atencion = future_atencion.result()

        # Agregamos el texto a la imagen
        print(emocion)
        print(type(emocion))
        if emocion is not None:
            texto_emocion = emocion
            color_emocion = (0, 255, 0)
        else:
            texto_emocion = "No se detecta la cara"
            color_emocion = (0, 0, 255)

        if atencion:
            color_atencion = (0, 255, 0)
        else:
            color_atencion = (0, 0, 255)

        cv2.putText(frame, texto_emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_emocion, 2)
        cv2.putText(frame, text_atencion, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color_atencion, 2)
        cv2.putText(frame, str(self.__segundo_actual()), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Detección de Caras', frame)
        # Terminamos el proceso si se ha interrumpido
        if self.__terminar_proceso():
            self._cap.release()
            cv2.destroyAllWindows()
            self.__recabar_estadisticas()
            self._gestorAtencion.terminar_escaneo(self.__segundo_actual())
            self._gestorEmociones.terminar_escaneo(self.__segundo_actual())

            # ELIMINAR
            self.pintar_datos()
            return False
        else:
            return True

    """"
        Calculamos el tiempo que lleva la cámara encendida.
            return: int
                
    """
    def __segundo_actual(self):
        return int(time.time() - self._tiempoInicio)

    """
        Cargamos los datos recabados en la clase de estadisticas
    """
    def __recabar_estadisticas(self):

        self._estadisticas.set_tiempototal(self.__segundo_actual())
        self._estadisticas.set_fechahorafin(datetime.now())
        total_emociones = self._gestorEmociones.get_tiempototalemocion()
        self._estadisticas.convertir_JSON_emociones(self._gestorEmociones.get_intervalosemociones())
        self._estadisticas.set_enfadadototal(total_emociones[Emociones.ENFADO.value])
        self._estadisticas.set_disgustadototal(total_emociones[Emociones.DISGUSTADO.value])
        self._estadisticas.set_miedosototal(total_emociones[Emociones.MIEDOSO.value])
        self._estadisticas.set_contentototal(total_emociones[Emociones.CONTENTO.value])
        self._estadisticas.set_tristetotal(total_emociones[Emociones.TRISTE.value])
        self._estadisticas.set_sorprendidototal(total_emociones[Emociones.SORPRENDIDO.value])
        self._estadisticas.set_neutrototal(total_emociones[Emociones.NEUTRO.value])

        self._estadisticas.convertir_JSON_atencion(self._gestorAtencion.get_intervalosatencion())
        self._estadisticas.set_atenciontotal(self._gestorAtencion.get_tiempototalatencion())




    """
        Evaluamos si el usuario ha terminado el proceso
        Return: boolean
            True si se ha terminado
            False si no
    """

    def __terminar_proceso(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    """ELIMINAAAAARRR
    """

    def pintar_datos(self):
        self.cabecera_end()
        self.imprimir_estadisticas_emociones()
        self.imprimir_estadisticas_atencion()

    def imprimir_estadisticas_emociones(self):
        print("\n" * 2)
        print("EMOCIONES:")
        intervalos_emociones = self._gestorEmociones.get_intervalosemociones()
        tiempototal_emocion = self._gestorEmociones.get_tiempototalemocion()
        for emotion in Emociones:
            print("\t-" + emotion.name, end="")
            print(intervalos_emociones[emotion.value])
            print("\tTiempo total: ", end="")
            print(tiempototal_emocion[emotion.value])

    def imprimir_estadisticas_atencion(self):
        print("\n" * 2)
        print("ATENCION:")
        intervalos_atencion = self._gestorAtencion.get_intervalosatencion()
        tiempototal_atencion = self._gestorAtencion.get_tiempototalatencion()
        print("\tIntervalos: ", end="")
        print(intervalos_atencion)
        print("\tTiempo total: ", end="")
        print(tiempototal_atencion)

    def cabecera_end(self):
        end = [
            "****** ***      ** *****",
            "**     ** **    ** **   **",
            "****** **   **  ** **    **",
            "**     **    ** ** **   **",
            "****** **     **** *****"
        ]

        print("\n" * 5)

        for linea in end:
            print(linea)

        print("\n" * 2)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~RESULTADOS~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
