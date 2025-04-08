from enum import Enum

"""
Listamos las emociones que vamos a reconocer,
de manera que cada emoción la asociamos a un numero entero 
para facilitar los cálculos.

"""


class Emociones(Enum):
    ENOJADO = 'angry'
    DISGUSTADO = 'disgust'
    MIEDO = 'fear'
    FELIZ = 'happy'
    TRISTE = 'sad'
    SORPRENDIDO = 'surprise'
    NEUTRO = 'neutral'
