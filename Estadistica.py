from Emociones import Emociones
import numpy as np
import time
import json


class Estadistica:
    def __init__(self, id_terapia, paciente_id, terapeuta_id, enfadado, enfadadototal,
                 disgustado, disgustadototal, miedoso, miedosototal, contento, contentototal,
                 triste, tristetotal, sorprendido, sorprendidototal, neutro, neutrototal, atencion, atenciontotal,
                 fechahoracomienzo, fechahorafin, tiempototal, observaciones):
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
        self._fechahoracomienzo = fechahoracomienzo
        self._fechahorafin = fechahorafin
        self._tiempototal = tiempototal
        self._observaciones = observaciones

    """
        Inicializamos la clase con los valores mínimos para irlos rellenando al final de la terapia
    """

    @classmethod
    def init_minimo(cls, paciente_id, terapeuta_id, fechahoracomienzo):
        print("[ESTADISTICA] Creamos estadística minima")
        return cls(None, paciente_id, terapeuta_id, None, 0,
                   None, 0, None, 0, None, 0,
                   None, 0, None, 0, None, 0, None, 0,
                   fechahoracomienzo, None, 0, "")

    # ********* GETTERS ***********

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

    def get_fechahoracomienzo(self):
        return self._fechahoracomienzo

    def get_fechahorafin(self):
        return self._fechahorafin

    def get_tiempototal(self):
        return self._tiempototal

    def get_observaciones(self):
        return self._observaciones

    # ********** SETTERS ***********

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

    def set_fechahoracomienzo(self, value):
        self._fechahoracomienzo = value

    def set_fechahorafin(self, value):
        self._fechahorafin = value

    def set_tiempototal(self, value):
        self._tiempototal = value

    def set_observaciones(self, value):
        self._observaciones = value

    # Metodos de la clase
    """
        Como nosotros recogemos los datos como una matriz, ahora tenemos que convertirlos a JSON
    """
    def convertir_JSON_emociones(self, intervalos_emociones):
        for emo in Emociones:
            emocion = emo.value
            texto = ''
            for intervalo in intervalos_emociones[emocion]:
                inicio, final = intervalo
                texto += '{"inicio":' + str(inicio) + ', "fin":' + str(final) + ' }, '
            # Eliminamos los dos últimos carácteres porque serán una coma y un espacio
            texto = texto[:-2]
            if emocion == Emociones.ENFADO:
                self._enfadado = "[" + texto + "]"
            elif emocion == Emociones.DISGUSTADO:
                self._disgustado = "[" + texto + "]"
            elif emocion == Emociones.MIEDOSO:
                self._miedoso = "[" + texto + "]"
            elif emocion == Emociones.CONTENTO:
                self._contento = "[" + texto + "]"
            elif emocion == Emociones.TRISTE:
                self._triste = "[" + texto + "]"
            elif emocion == Emociones.SORPRENDIDO:
                self._sorprendido = "[" + texto + "]"
            elif emocion == Emociones.NEUTRO:
                self._neutro = "[" + texto + "]"
            # Ignoramos si el valor es NONE
    """
            Como nosotros recogemos los datos como un a matriz, ahora tenemos que convertirlos a JSON
    """
    def convertir_JSON_atencion(self, intervalos_atencion):
        texto = ''
        for intervalo in intervalos_atencion:
            inicio, final = intervalo
            texto += '{"inicio":' + str(inicio) + ' "fin":' + str(final) + ' }, '
        # Eliminamos los dos últimos carácteres porque serán una coma y un espacio
        texto = texto[:-2]
        self._atencion = "[" + texto + "]"
