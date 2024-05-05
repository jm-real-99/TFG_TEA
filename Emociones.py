from enum import Enum

"""
Listamos las emociones que vamos a reconocer,
de manera que cada emoción la asociamos a un numero entero 
para facilitar los cálculos.

"""


class Emociones(Enum):
    ENFADO = 1
    DISGUSTADO = 2
    MIEDOSO = 2
    CONTENTO = 4
    TRISTE = 5
    SORPRENDIDO = 6
    NEUTRO = 7
