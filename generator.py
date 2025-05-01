import numpy as np

def generar_datos(distribucion, n, **kwargs):
    if distribucion == "uniforme":
        a = kwargs.get("a", 0)
        b = kwargs.get("b", 1)
        return np.random.uniform(a, b, n)
    elif distribucion == "exponencial":
        lambd = kwargs.get("lambd", 1)
        return np.random.exponential(1 / lambd, n)
    elif distribucion == "normal":
        media = kwargs.get("mu", 0)
        sigma = kwargs.get("sigma", 1)
        return np.random.normal(media, sigma, n)
    else:
        raise ValueError("Distribución no válida.")
