from Estadistica import Estadistica
from Emociones import Emociones


class Calculo_estadisticas():
    def __init__(self, estadisticas):
        self.estadisticas = estadisticas
        # Primero vamos a mostrar estadísticas generales
        self.num_terapias = 0
        self.totalenfadado = 0
        self.totaldisgustado = 0
        self.totalmiedoso = 0
        self.totalcontento = 0
        self.totaltriste = 0
        self.totalsorprendido = 0
        self.totalneutro = 0
        self.totalatencion = 0
        self.apariciones_enfadado = 0
        self.apariciones_disgustado = 0
        self.apariciones_miedoso = 0
        self.apariciones_contento = 0
        self.apariciones_triste = 0
        self.apariciones_sorprendido = 0
        self.apariciones_neutro = 0
        self.apariciones_atencion = 0
        self.terapia_max_enfadado = 0
        self.terapia_max_disgustado = 0
        self.terapia_max_miedoso = 0
        self.terapia_max_contento = 0
        self.terapia_max_triste = 0
        self.terapia_max_sorprendido = 0
        self.terapia_max_neutro = 0
        self.terapia_max_atencion = 0
        self.mins_total_atencion = 0
        self.porcentaje_enfadado = 0
        self.porcentaje_disgustado = 0
        self.porcentaje_miedoso = 0
        self.porcentaje_contento = 0
        self.porcentaje_triste = 0
        self.porcentaje_sorprendido = 0
        self.porcentaje_neutro = 0
        self.porcentaje_atencion = 0
        self.mejora_inicio_expresion_emociones = 0
        self.mejora_tendencia_expresion_emociones = 0
        self.mejora_inicio_atencion = 0
        self.mejora_tendencia_atencion = 0
        self.emocion_mas_expresada = None

    def inicializarDatos(self):
        self.num_terapias = self.estadisticas.size()
        tiempo_total_terapias = 0
        mejora_atencion = []
        mejora_emociones = []
        for estadistica in self.estadisticas:
            tiempo_total_terapias += estadistica.get_tiempototal()

            self.totalenfadado += estadistica.get_enfadado_total()
            self.totaldisgustado += estadistica.get_disgustadototal()
            self.totalmiedoso += estadistica.get_miedosototal()
            self.totalcontento += estadistica.get_contentototal()
            self.totaltriste += estadistica.get_tristetotal()
            self.totalsorprendido += estadistica.get_sorprendidototal()
            self.totalneutro += estadistica.get_neutrototal()
            self.totalatencion += estadistica.get_atenciontotal()

            apariciones_enfadado = estadistica.get_enfadado().count("inicio")
            apariciones_disgustado = estadistica.get_disgustado().count("inicio")
            apariciones_miedoso = estadistica.get_miedoso().count("inicio")
            apariciones_contento = estadistica.get_contento().count("inicio")
            apariciones_triste = estadistica.get_triste().count("inicio")
            apariciones_sorprendido = estadistica.get_sorprendido().count("inicio")
            apariciones_neutro = estadistica.get_neutro().count("inicio")
            apariciones_atencion = estadistica.get_atencion().count("inicio")

            self.apariciones_enfadado += apariciones_enfadado
            self.apariciones_disgustado += apariciones_disgustado
            self.apariciones_miedoso += apariciones_miedoso
            self.apariciones_contento += apariciones_contento
            self.apariciones_triste += apariciones_triste
            self.apariciones_sorprendido += apariciones_sorprendido
            self.apariciones_neutro += apariciones_neutro
            self.apariciones_atencion += apariciones_atencion

            self.terapia_max_enfadado = apariciones_enfadado if apariciones_enfadado > self.terapia_max_enfadado else (
                self.terapia_max_enfadado)
            self.terapia_max_disgustado = apariciones_disgustado if (apariciones_disgustado >
                                                                     self.terapia_max_disgustado) else (
                self.terapia_max_disgustado)
            self.terapia_max_miedoso = apariciones_miedoso if apariciones_miedoso > self.terapia_max_miedoso else (
                self.terapia_max_miedoso)
            self.terapia_max_contento = apariciones_contento if apariciones_contento > self.terapia_max_contento else (
                self.terapia_max_contento)
            self.terapia_max_triste = apariciones_triste if apariciones_triste > self.terapia_max_triste else (
                self.terapia_max_triste)
            self.terapia_max_sorprendido = apariciones_sorprendido if (apariciones_sorprendido >
                                                                       self.terapia_max_sorprendido) else (
                self.terapia_max_sorprendido)
            self.terapia_max_neutro = apariciones_neutro if apariciones_neutro > self.terapia_max_neutro else (
                self.terapia_max_neutro)
            self.terapia_max_atencion = apariciones_atencion if apariciones_atencion > self.terapia_max_atencion else (
                self.terapia_max_atencion)

            # Calculamos el % de emociones detectadas a través de todas las terapias, es decir, que no hayan sido
            # neutras
            emociones_expr = 100 - ((self.totalneutro * estadistica.get_tiempototal)/100 )
            mejora_emociones.append(emociones_expr)

            # Calculamos el % de atención prestada a través de todas las terapias
            atencion_expr = (self.totalatencion * estadistica.get_tiempototal) / 100
            mejora_atencion.append(atencion_expr)

        self.mins_total_atencion = self.totalatencion / 60

        total_emociones = (self.totalenfadado + self.totaldisgustado + self.totalmiedoso + self.totalcontento +
                           self.totaltriste + self.totalsorprendido + self.totalneutro + self.totalatencion)
        self.porcentaje_enfadado = (self.totalenfadado * total_emociones) / 100
        self.porcentaje_disgustado = (self.porcentaje_disgustado * total_emociones) / 100
        self.porcentaje_miedoso = (self.porcentaje_miedoso * total_emociones) / 100
        self.porcentaje_contento = (self.porcentaje_contento * total_emociones) / 100
        self.porcentaje_triste = (self.porcentaje_triste * total_emociones) / 100
        self.porcentaje_sorprendido = (self.porcentaje_sorprendido * total_emociones) / 100
        self.porcentaje_neutro = (self.porcentaje_neutro * total_emociones) / 100
        self.porcentaje_atencion = (self.porcentaje_atencion * tiempo_total_terapias) / 100

        # Obtenemos la emoción más expresada según el porcentaje total
        cuentamax = 0
        if self.porcentaje_enfadado > cuentamax:
            self.emocion_mas_expresada = Emociones.ENFADO
            cuentamax = self.porcentaje_enfadado
        if self.porcentaje_disgustado > cuentamax:
            self.emocion_mas_expresada = Emociones.DISGUSTADO
            cuentamax = self.porcentaje_disgustado
        if self.porcentaje_miedoso > cuentamax:
            self.emocion_mas_expresada = Emociones.MIEDOSO
            cuentamax = self.porcentaje_miedoso
        if self.porcentaje_contento > cuentamax:
            self.emocion_mas_expresada = Emociones.CONTENTO
            cuentamax = self.porcentaje_contento
        if self.porcentaje_triste > cuentamax:
            self.emocion_mas_expresada = Emociones.TRISTE
            cuentamax = self.porcentaje_triste
        if self.porcentaje_sorprendido > cuentamax:
            self.emocion_mas_expresada = Emociones.SORPRENDIDO
            cuentamax = self.porcentaje_sorprendido
        if self.porcentaje_neutro > cuentamax:
            self.emocion_mas_expresada = Emociones.NEUTRO

        # Los siguientes datos solo se pueden calcular si tenemos más de 1 terapia, por lo que si no las tenemos
        # no podemos calcularlas y terminamos el método aquí
        if self.num_terapias < 1:
            return None

        # Obtenemos la mejora total de la expresión de emoiones, con la diferencia de la primera terapia y la última
        self.mejora_inicio_expresion_emociones = mejora_emociones[len(mejora_emociones)-1] - mejora_emociones[0]
        # Obtenemos la mejora total de la atención, con la diferencia de la primera terapia y la última
        self.mejora_inicio_atencion = mejora_atencion[len(mejora_atencion) - 1] - mejora_atencion[0]

        # Los siguientes datos solo se pueden calcular si tenemos más de 2 terapias, por lo que si no las tenemos
        # no podemos calcularlas y terminamos el método aquí
        if self.num_terapias < 2:
            return None

        # Obtenemos el incremento medio de expresión de emociones a través de todas las terapias
        incremento = []
        for i in (1, len(mejora_emociones)):
            incremento.append(mejora_emociones[i]-mejora_emociones[i-1])

        self.mejora_inicio_expresion_emociones = sum(incremento) / len(incremento)

        # Obtenemos el incremento medio de la atención a través de todas las terapias
        incremento = []
        for i in (1, len(mejora_atencion)):
            incremento.append(mejora_atencion[i] - mejora_atencion[i - 1])

        self.mejora_tendencia_atencion = sum(incremento) / len(incremento)

