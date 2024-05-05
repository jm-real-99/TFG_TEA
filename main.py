from Camara import Camara
import cv2

"""
    Enumera las cámaras disponibles y muestra información sobre cada una.
"""


def listar_camaras():
    num_camara = 0
    while True:
        cap = cv2.VideoCapture(num_camara)
        if not cap.isOpened():
            break
        _, frame = cap.read()
        h, w = frame.shape[:2]
        print(f"Cámara {num_camara}: {w}x{h}")
        cap.release()
        num_camara += 1
    return int(input("Introduce camara: "))


camara = Camara(listar_camaras())

while (True):
    end = camara.read_frame()
    if not (end):
        break
