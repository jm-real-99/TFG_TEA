import Camara

camara = Camara(2)

while (True):
    end = camara.read_frame()
    if not(end):
        break





