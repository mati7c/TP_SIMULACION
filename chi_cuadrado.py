import numpy as np
import math

def obtener_tabla_chi_cuadrado(datos, intervalos, distribucion):
    conteos, bordes_intervalos = np.histogram(datos, bins=intervalos)
    tabla_frecuencias = {"Intervalo": [], "Frecuencia Observada": [], "Frecuencia Esperada": []}

    if distribucion == "exponencial":
        lamb = 1 / np.mean(datos)
    elif distribucion == "normal":
        media = sum(datos) / len(datos)
        sigma_suma = sum((x - media) ** 2 for x in datos)
        sigma = np.sqrt(sigma_suma / (len(datos) - 1))

    bandera_int_inf = 0
    fe_acumulada = 0
    conteo_acumulado = 0

    for i in range(len(conteos)):
        if distribucion == "uniforme":
            fe = len(datos) / intervalos
        elif distribucion == "exponencial":
            fe = ((1 - math.exp(-1 * lamb * bordes_intervalos[i + 1])) -
                  (1 - math.exp(-1 * lamb * bordes_intervalos[i]))) * len(datos)
        else:
            marca_clase = (bordes_intervalos[i + 1] + bordes_intervalos[i]) / 2
            diferencia = bordes_intervalos[i + 1] - bordes_intervalos[i]
            fe = (np.exp(-0.5 * ((marca_clase - media) / sigma) ** 2) /
                  (sigma * np.sqrt(2 * np.pi))) * diferencia * len(datos)

        if fe >= 5 and bandera_int_inf == 0:
            intervalo = f"{bordes_intervalos[i]:.4f} - {bordes_intervalos[i+1]:.4f}"
            tabla_frecuencias["Intervalo"].append(intervalo)
            tabla_frecuencias["Frecuencia Observada"].append(conteos[i])
            tabla_frecuencias["Frecuencia Esperada"].append(fe)
        else:
            fe_acumulada += fe
            conteo_acumulado += conteos[i]
            bandera_int_inf += 1

            if fe_acumulada >= 5:
                intervalo = f"{bordes_intervalos[i-bandera_int_inf+1]:.4f} - {bordes_intervalos[i+1]:.4f}"
                tabla_frecuencias["Intervalo"].append(intervalo)
                tabla_frecuencias["Frecuencia Observada"].append(conteo_acumulado)
                tabla_frecuencias["Frecuencia Esperada"].append(fe_acumulada)
                bandera_int_inf = 0
                fe_acumulada = 0
                conteo_acumulado = 0

    return tabla_frecuencias

def calcular_chi_tabla(tabla_chi):
    chi = 0
    for fo, fe in zip(tabla_chi["Frecuencia Observada"], tabla_chi["Frecuencia Esperada"]):
        chi += ((fe - fo) ** 2) / fe
    return chi