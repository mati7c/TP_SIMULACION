import numpy as np
import random

def generar_datos(distribucion, n, **kwargs):
    if distribucion == "uniforme":
        a = kwargs.get("a", 0)
        b = kwargs.get("b", 1)
        datos = []
        for i in range(n):
            x = a + (random.random() * (b-a))
            datos.append(x)
        return datos
        #return np.random.uniform(a, b, n)
    elif distribucion == "exponencial":
        lambd = kwargs.get("lambd", 1)
        datos = []
        for i in range (n):
            x = (-1/lambd) * (np.log(1-random.random()))
            datos.append(x)
        return datos
        #return np.random.exponential(1 / lambd, n)
    elif distribucion == "normal":
        media = kwargs.get("mu", 0)
        sigma = kwargs.get("sigma", 1)
        datos = []
        for i in range(n//2):
            rnd1 = random.random()
            rnd2 = random.random()
            x1 = ((np.sqrt((-2) * np.log(rnd1)) * np.cos(2 * np.pi * rnd2)) * sigma) + media
            x2 = ((np.sqrt((-2) * np.log(rnd1)) * np.sin(2 * np.pi * rnd2)) * sigma) + media
            datos.append(x1)
            datos.append(x2)
            if n % 2 != 0:
                # Si n es impar, agrego 1 más al final (porque el for tiene división entera)
                x = ((np.sqrt((-2) * np.log(rnd1)) * np.cos(2 * np.pi * rnd2)) * sigma) + media
                datos.append(x)
        return datos
        #return np.random.normal(media, sigma, n)
    else:
        raise ValueError("Distribución no válida.")
