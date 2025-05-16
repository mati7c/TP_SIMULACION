import matplotlib.pyplot as plt
import pandas as pd

def graficar_histograma(datos, bins):
    plt.ion()
    plt.figure("Histograma")
    plt.hist(datos, bins=bins, edgecolor='black')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)

def mostrar_tabla_frecuencias(datos, bins):
    series = pd.Series(datos)
    categorias = pd.cut(series, bins=bins)
    conteo = categorias.value_counts(sort=False)
    return list(zip(conteo.index.astype(str), conteo.values))