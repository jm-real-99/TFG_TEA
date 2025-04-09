from enum import Enum

"""
Listamos las emociones que vamos a reconocer,
de manera que cada emoción la asociamos a un numero entero 
para facilitar los cálculos.

"""


class Emociones(Enum):
    ENFADO = 'angry'
    DISGUSTADO = 'disgust'
    MIEDOSO = 'fear'
    CONTENTO = 'happy'
    TRISTE = 'sad'
    SORPRENDIDO = 'surprise'
    NEUTRO = 'neutral'
    NONE = 'none'
