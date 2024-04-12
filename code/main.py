import time
import random

tiempoInicio = time.time()
n = random.randint(1,5)
for i in range(n+1):
    print(i)
    time.sleep(1)
tiempoFinal = time.time()
print("tiempo: "+str(tiempoFinal))
t = int(tiempoFinal - tiempoInicio)
print("La funcion ha tardado "+str(t)+" segundos")


