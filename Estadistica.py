from Emociones import Emociones
import numpy as np
import time
import json

from LoggerManager import LoggerManager


class Estadistica:
    """
    Clase de las estadísticas. Contiene toda la información recabada a lo largo de una terapia.
    """
    def __init__(self, id_terapia, paciente_id, terapeuta_id, enfadado, enfadadototal,
                 disgustado, disgustadototal, miedoso, miedosototal, contento, contentototal,
                 triste, tristetotal, sorprendido, sorprendidototal, neutro, neutrototal, atencion, atenciontotal, fecha,
                 horacomienzo, horafin, tiempototal, observaciones):
        # Inicializamos los logs:
        self._logger = LoggerManager.get_logger()

        self._id_terapia = id_terapia
        self._paciente_id = paciente_id
        self._terapeuta_id = terapeuta_id
        self._enfadado = enfadado
        self._enfadadototal = enfadadototal
        self._disgustado = disgustado
        self._disgustadototal = disgustadototal
        self._miedoso = miedoso
        self._miedosototal = miedosototal
        self._contento = contento
        self._contentototal = contentototal
        self._triste = triste
        self._tristetotal = tristetotal
        self._sorprendido = sorprendido
        self._sorprendidototal = sorprendidototal
        self._neutro = neutro
        self._neutrototal = neutrototal
        self._atencion = atencion
        self._atenciontotal = atenciontotal
        self._fecha = fecha
        self._horacomienzo = horacomienzo
        self._horafin = horafin
        self._tiempototal = tiempototal
        self._observaciones = observaciones

    @classmethod
    def init_minimo(cls, paciente_id, terapeuta_id, fecha, hora_comienzo):
        """
        Inicializamos la clase con los valores mínimos para irlos rellenando al final de la terapia
        @param paciente_id: Identificador del paciente que está llevando a cabo la terapia
         y por tanto asociada a esta estadística
        @param terapeuta_id: Identificador del terpeuta que está llevando a cabo la terapia
         y por tanto asociada a esta estadística
        @param fecha: Fecha en la que se está realizando la terapia
        @param hora_comienzo: Hora comienzo de la terapia
        @return: Entidad Estadística creada.
        """
        return cls(None, paciente_id, terapeuta_id, None, 0,
                   None, 0, None, 0, None, 0,
                   None, 0, None, 0, None, 0, None, 0,fecha,
                   hora_comienzo, None, 0, "")


    """ **************************************************************************************
        ************************************** GETTERS ***************************************
        ************************************************************************************** """

    def get_id_terapia(self):
        return self._id_terapia

    def get_paciente_id(self):
        return self._paciente_id

    def get_terapeuta_id(self):
        return self._terapeuta_id

    def get_enfadado(self):
        return self._enfadado

    def get_enfadado_total(self):
        return self._enfadadototal

    def get_disgustado(self):
        return self._disgustado

    def get_disgustadototal(self):
        return self._disgustadototal

    def get_miedoso(self):
        return self._miedoso

    def get_miedosototal(self):
        return self._miedosototal

    def get_contento(self):
        return self._contento

    def get_contentototal(self):
        return self._contentototal

    def get_triste(self):
        return self._triste

    def get_tristetotal(self):
        return self._tristetotal

    def get_sorprendido(self):
        return self._sorprendido

    def get_sorprendidototal(self):
        return self._sorprendidototal

    def get_neutro(self):
        return self._neutro

    def get_neutrototal(self):
        return self._neutrototal

    def get_atencion(self):
        return self._atencion

    def get_atenciontotal(self):
        return self._atenciontotal

    def get_fecha(self):
        return self._fecha

    def get_horacomienzo(self):
        return self._horacomienzo

    def get_horafin(self):
        return self._horafin

    def get_tiempototal(self):
        return self._tiempototal

    def get_observaciones(self):
        return self._observaciones

    """ **************************************************************************************
        ************************************** SETTERS ***************************************
        ************************************************************************************** """

    def set_id_terapia(self, value):
        self._id_terapia = value

    def set_paciente_id(self, value):
        self._paciente_id = value

    def set_terapeuta_id(self, value):
        self._terapeuta_id = value

    def set_enfadado(self, value):
        self._enfadado = value

    def set_enfadadototal(self, value):
        self._enfadadototal = value

    def set_disgustado(self, value):
        self._disgustado = value

    def set_disgustadototal(self, value):
        self._disgustadototal = value

    def set_miedoso(self, value):
        self._miedoso = value

    def set_miedosototal(self, value):
        self._miedosototal = value

    def set_contento(self, value):
        self._contento = value

    def set_contentototal(self, value):
        self._contentototal = value

    def set_triste(self, value):
        self._triste = value

    def set_tristetotal(self, value):
        self._tristetotal = value

    def set_sorprendido(self, value):
        self._sorprendido = value

    def set_sorprendidototal(self, value):
        self._sorprendidototal = value

    def set_neutro(self, value):
        self._neutro = value

    def set_neutrototal(self, value):
        self._neutrototal = value

    def set_atencion(self, value):
        self._atencion = value

    def set_atenciontotal(self, value):
        self._atenciontotal = value

    def set_fecha(self,value):
        self._fecha = value

    def set__horacomienzo(self, value):
        self._horacomienzo = value

    def set_horafin(self, value):
        self._horafin = value

    def set_tiempototal(self, value):
        self._tiempototal = value

    def set_observaciones(self, value):
        self._observaciones = value

    # Metodos de la clase
    """
        Como nosotros recogemos los datos como una matriz, ahora tenemos que convertirlos a JSON
    """
    def convertir_JSON_emociones(self, intervalos_emociones):
        """
        Transformamos los diccionarios que se han recogido durante las terapias a JSON para almacenarlos en BD
        @param intervalos_emociones: Diccionario con las emociones expresadas a lo largo de la terapia
        @return: None
        """
        self._logger.info("[ESTADÍSTICAS] Convertimos las emociones a formato JSON")
        for emo in Emociones:
            emocion = emo.value
            texto = ''
            for intervalo in intervalos_emociones[emocion]:
                inicio, final = intervalo
                texto += '{"inicio":' + str(inicio) + ', "fin":' + str(final) + ' }, '
            # Eliminamos los dos últimos carácteres porque serán una coma y un espacio
            texto = texto[:-2]
            if emo == Emociones.ENFADO:
                self._enfadado = "[" + texto + "]"
            elif emo == Emociones.DISGUSTADO:
                self._disgustado = "[" + texto + "]"
            elif emo == Emociones.MIEDOSO:
                self._miedoso = "[" + texto + "]"
            elif emo == Emociones.CONTENTO:
                self._contento = "[" + texto + "]"
            elif emo == Emociones.TRISTE:
                self._triste = "[" + texto + "]"
            elif emo == Emociones.SORPRENDIDO:
                self._sorprendido = "[" + texto + "]"
            elif emo == Emociones.NEUTRO:
                self._neutro = "[" + texto + "]"
            # Ignoramos si el valor es NONE
        self._logger.info("[ESTADÍSTICAS] Convertidas las emociones a formato JSON exitosamente")
    """
            Como nosotros recogemos los datos como un a matriz, ahora tenemos que convertirlos a JSON
    """
    def convertir_JSON_atencion(self, intervalos_atencion):
        """
        Transformamos los diccionarios que se han recogido durante las terapias a JSON para almacenarlos en BD
        @param intervalos_atencion: Diccionario con los intervalos de la atención
        @return: None
        """
        self._logger.info("[ESTADÍSTICAS] Convertimos la atención a formato JSON")
        texto = ''
        for intervalo in intervalos_atencion:
            inicio, final = intervalo
            texto += '{"inicio":' + str(inicio) + ', "fin":' + str(final) + ' }, '
        # Eliminamos los dos últimos carácteres porque serán una coma y un espacio
        texto = texto[:-2]
        self._atencion = "[" + texto + "]"
        self._logger.info("[ESTADÍSTICAS] Convertida las atención a formato JSON con éxito")

    def get_emocion_mas_expresada(self):
        """
        Obtenemos la emoción más expresada
        @return: Emoción más expresada
        """
        self._logger.info("[ESTADÍSTICAS] Obtenemos la expresión más expresada")
        emociones = [(self._contentototal, Emociones.CONTENTO), (self._disgustadototal, Emociones.DISGUSTADO),
                     (self._enfadadototal, Emociones.ENFADO), (self._tristetotal, Emociones.TRISTE),
                     (self._miedosototal, Emociones.MIEDOSO), (self._sorprendidototal, Emociones.SORPRENDIDO),
                     (self._neutrototal, Emociones.NEUTRO)]
        return max(emociones, key=lambda x: x[0])[1]

    def get_emociones_porcentajes(self):
        """
        Obtenemos los porcentajes de las emociones
        @return: Array de los porcentajes para cada emoción
        """
        self._logger.info("[ESTADÍSTICAS] Obtenemos los porcentajes de las emociones")
        return [self._enfadadototal/self._tiempototal , self._disgustadototal/self._tiempototal ,
                self._miedosototal/self._tiempototal , self._contentototal/self._tiempototal ,
                self._tristetotal/self._tiempototal , self._sorprendidototal/self._tiempototal ,
                self._neutrototal/self._tiempototal]
