from Emociones import Emociones

class GestorEmociones:
    def __init__(self):
        #Mediante esta variable controlaremos cuál es la emoción actual y sabremos si esta ha cambiado
        self.emocionActual = 0
        #Mediante esta variable sabremos cuando hemos empezado a detectar una emoción.
        self.t_inicioEmocion = 0
        #Diccionario clave-valor donde se almacenará una dupla (Ti,Tf) donde Ti es el segundo inicial del intervalo dónde se ha mostrado la emoción y Tf el final. Esto se guardará en la emoción correspondiente.
        self.intervalosEmociones = {emotion: [] for emotion in Emociones}
        #Diccionario clave-valor donde almacenaremos el tiempo total quie se expresa la emoción a lo largo de la terapia, esto nos permitirá ahorrar tiempo de cómputo a la hora de calcular las estadísticas.
        self.tiempoTotalEmocion = {emotion: [] for emotion in Emociones}


    """
        Agregamos un intervalo con la emoción específica
        Args:
            comienzo (float): Tiempo de inicio en segundos.
            fin (float): Tiempo de fin en segundos.
            emocion (int): Emoción detectada del enum Emociones
    """
    def add_emotion_interval(self,fin):
        self.intervalosEmociones[self.emocionActual].append((self.t_inicioEmocion, fin))

    """
        Recibimos la emoción en el segundo actual.
        Args:
            tiempo (float): Tiempo actual
             emocion (int): Emoción detectada del enum Emociones
    """
    def registrar_emocion(self,tiempo,emocion):
        #Si hemos cambiado de emocion entonces hacemos la gestión correspondiente.
        if(emocion!=self.emocionActual):
            self.cambiar_emocion(tiempo,emocion)
        #Si no hemos cambiado la emoción sumamos un número a su contador.
        else:
            self.tiempoTotalEmocion[emocion]+=1

    """
        Actualizamos las variables actuales referidas a la emocion actual
        Args:
            tiempo (float): Tiempo actual
            emocion (int): Emoción detectada del enum Emociones
    """
    def cambiar_emocion(self, tiempo, emocion):
        self.add_emotion_interval(tiempo)
        self.t_inicioEmocion = tiempo
        self.emocionActual = emocion
