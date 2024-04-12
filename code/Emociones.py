from enum import Enum

"""
Listamos las emociones que vamos a reconocer,
de manera que cada emoción la asociamos a un numero entero 
para facilitar los cálculos.

"""
class Emociones(Enum):
    FELICIDAD = 1
    TRISTE = 2
    NEUTRO = 3
