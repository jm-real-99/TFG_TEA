from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random

barrier = threading.Barrier(2)

def tarea_x():
    print("Tarea X: trabajando...")
    zzzz = random.randint(0, 5)
    time.sleep(zzzz)
    # barrier.wait()
    print("Tarea X: dormido durante "+str(zzzz)+"s")
    return zzzz

def tarea_y():
    print("Tarea Y: trabajando...")
    zzzz = random.randint(0, 5)
    time.sleep(zzzz)
    # barrier.wait()
    print("Tarea Y: dormido durante " + str(zzzz) + "s")
    return zzzz

def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        i=1
        while True:
            # Lanzamos las dos tareas y obtenemos los objetos Future
            future_x = executor.submit(tarea_x)
            future_y = executor.submit(tarea_y)

            # Esperamos a que ambas terminen
            duracion_x = future_x.result()
            duracion_y = future_y.result()

            print("*********************")
            print("X:"+str(duracion_x))
            print("Y:"+str(duracion_y))
            print("Iteracion: "+str(i))
            print("*********************")
            i+=1
            time.sleep(0.5)

if __name__ == "__main__":
    main()
