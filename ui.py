import tkinter as tk
from tkinter import ttk, messagebox
from generator import generar_datos
from plotter import graficar_histograma, mostrar_tabla_frecuencias

def actualizar_parametros(event=None):
    dist = distribucion_var.get()
    if dist == "Uniforme":
        label_param1.config(text="a:")
        label_param2.config(text="b:")
        entrada_param1.grid()
        entrada_param2.grid()
        label_param2.grid()
    elif dist == "Exponencial":
        label_param1.config(text="λ (lambda):")
        entrada_param1.grid()
        entrada_param2.grid_remove()
        label_param2.grid_remove()
    elif dist == "Normal":
        label_param1.config(text="μ (mu):")
        label_param2.config(text="σ (sigma):")
        entrada_param1.grid()
        entrada_param2.grid()
        label_param2.grid()
    else:
        entrada_param1.grid_remove()
        entrada_param2.grid_remove()
        label_param1.grid_remove()
        label_param2.grid_remove()

def ejecutar():
    try:
        dist = distribucion_var.get()
        size = int(entrada_muestra.get())
        bins = int(bins_var.get())

        if size < 1 or size > 1_000_000:
            raise ValueError("El tamaño de muestra debe estar entre 1 y 1.000.000")

        if dist == "Uniforme":
            a = float(entrada_param1.get())
            b = float(entrada_param2.get())
            if a >= b:
                raise ValueError("a debe ser menor que b")
            datos = generar_datos("uniforme", size, a=a, b=b)
        elif dist == "Exponencial":
            lambd = float(entrada_param1.get())
            if lambd <= 0:
                raise ValueError("Lambda debe ser mayor a cero")
            datos = generar_datos("exponencial", size, lambd=lambd)
        elif dist == "Normal":
            mu = float(entrada_param1.get())
            sigma = float(entrada_param2.get())
            if sigma <= 0:
                raise ValueError("Sigma(La desviación) debe ser mayor a cero")
            datos = generar_datos("normal", size, mu=mu, sigma=sigma)
        else:
            raise ValueError("Distribución no reconocida.")

        # Mostrar datos generados
        text_datos.delete("1.0", tk.END)
        text_datos.insert(tk.END, "\n".join(f"{x:.4f}" for x in datos[:]))

        # Mostrar tabla de frecuencias
        tabla = mostrar_tabla_frecuencias(datos, bins)
        text_tabla.delete("1.0", tk.END)
        for intervalo, freq in tabla:
            text_tabla.insert(tk.END, f"{intervalo}: {freq}\n")

        # Mostrar histograma
        graficar_histograma(datos, bins)

    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Ventana principal
ventana = tk.Tk()
ventana.title("Generador de Variables Aleatorias, Distribucion y Frecuencia")
ventana.geometry("800x400")

# Widgets
tk.Label(ventana, text="Distribución:").grid(row=0, column=0, sticky="w")
distribucion_var = ttk.Combobox(ventana, values=["Uniforme", "Exponencial", "Normal"], state="readonly")
distribucion_var.grid(row=0, column=1)
distribucion_var.current(0)
distribucion_var.bind("<<ComboboxSelected>>", actualizar_parametros)

tk.Label(ventana, text="Tamaño de muestra (1 a 1.000.000):").grid(row=1, column=0, sticky="w")
entrada_muestra = tk.Entry(ventana)
entrada_muestra.grid(row=1, column=1)

# Parámetros dinámicos
label_param1 = tk.Label(ventana, text="a:")
label_param1.grid(row=2, column=0, sticky="w")
entrada_param1 = tk.Entry(ventana)
entrada_param1.grid(row=2, column=1)

label_param2 = tk.Label(ventana, text="b:")
label_param2.grid(row=3, column=0, sticky="w")
entrada_param2 = tk.Entry(ventana)
entrada_param2.grid(row=3, column=1)

tk.Label(ventana, text="Cantidad de intervalos (bins):").grid(row=4, column=0, sticky="w")
bins_var = ttk.Combobox(ventana, values=[10, 15, 20, 25], state="readonly")
bins_var.grid(row=4, column=1)
bins_var.current(0)

tk.Button(ventana, text="Ejecutar", command=ejecutar).grid(row=5, column=1, pady=10)

# Resultados
tk.Label(ventana, text="Números Aleatorios Generados:").grid(row=6, column=0, sticky="w")
text_datos = tk.Text(ventana, height=10, width=50)
text_datos.grid(row=7, column=0, columnspan=2)

tk.Label(ventana, text="Tabla de Frecuencias:").grid(row=6, column=2, sticky="w")
text_tabla = tk.Text(ventana, height=10, width=50)
text_tabla.grid(row=7, column=2, columnspan=2)

# Llamar la función para inicializar correctamente
actualizar_parametros()

def iniciar_app():
    ventana.mainloop()
