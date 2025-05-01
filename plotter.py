import matplotlib.pyplot as plt
import pandas as pd

def graficar_histograma(datos, bins):
    plt.figure("Histograma")
    plt.hist(datos, bins=bins, edgecolor='black')
    plt.title("Histograma")
    plt.xlabel("Valores")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    plt.show()  # Esto abre una nueva ventana con el gráfico

def mostrar_tabla_frecuencias(datos, bins):
    series = pd.Series(datos)
    categorias = pd.cut(series, bins=bins)
    conteo = categorias.value_counts(sort=False)
    return list(zip(conteo.index.astype(str), conteo.values))
