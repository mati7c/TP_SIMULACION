from chi_cuadrado import obtener_tabla_chi_cuadrado, calcular_chi_tabla
from scipy.stats import chi2
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from generator import generar_datos
from plotter import graficar_histograma, mostrar_tabla_frecuencias

# Configuración de colores
PRIMARY_COLOR = "#2c3e50"  # Azul oscuro
SECONDARY_COLOR = "#3498db"  # Azul brillante
ACCENT_COLOR = "#e74c3c"  # Rojo
BG_COLOR = "#ecf0f1"  # Gris claro
FRAME_COLOR = "#ffffff"  # Blanco
BUTTON_COLOR = "#2ecc71"  # Verde
TEXT_BG = "#ffffff"  # Blanco
HIGHLIGHT_COLOR = "#f39c12"  # Naranja

# Configuración de fuentes
FONT = ("Segoe UI", 10)
TITLE_FONT = ("Segoe UI", 12, "bold")
HEADER_FONT = ("Segoe UI", 11, "bold")

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
            g_l = bins - 1
        elif dist == "Exponencial":
            lambd = float(entrada_param1.get())
            if lambd <= 0:
                raise ValueError("Lambda debe ser mayor a cero")
            datos = generar_datos("exponencial", size, lambd=lambd)
            g_l = bins - 2
        elif dist == "Normal":
            mu = float(entrada_param1.get())
            sigma = float(entrada_param2.get())
            if sigma <= 0:
                raise ValueError("Sigma (desviación) debe ser mayor a cero")
            datos = generar_datos("normal", size, mu=mu, sigma=sigma)
            g_l = bins - 3
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

        # Calcular Chi-cuadrado
        tabla_chi = obtener_tabla_chi_cuadrado(datos, bins, dist.lower())
        chi_valor = calcular_chi_tabla(tabla_chi)
        chi_critico = chi2.ppf(0.95, g_l)
        resultado = "NO HAY SUFICIENTE EVIDENCIA para rechazar la hipótesis nula" if chi_valor < chi_critico else "SE RECHAZA la hipótesis nula"

        text_chi.delete("1.0", tk.END)
        text_chi.insert(tk.END, f"Chi² calculado: {chi_valor:.4f}\n")
        text_chi.insert(tk.END, f"Chi² crítico (gl={g_l}, α=0.05): {chi_critico:.4f}\n")
        text_chi.insert(tk.END, f"Resultado: {resultado}")

        # Mostrar histograma
        graficar_histograma(datos, bins)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Variables Aleatorias - Distribución y Frecuencia")
ventana.geometry("1000x700")
ventana.configure(bg=BG_COLOR)
ventana.minsize(900, 600)

# Header con título
header = tk.Frame(ventana, bg=PRIMARY_COLOR, height=60)
header.pack(fill="x", padx=0, pady=0)
tk.Label(header, text="Generador de Variables Aleatorias", 
         font=("Segoe UI", 16, "bold"), fg="white", bg=PRIMARY_COLOR).pack(side="left", padx=20)

# Frame de configuración
config_frame = tk.LabelFrame(ventana, text=" CONFIGURACIÓN ", bg=FRAME_COLOR, 
                           font=TITLE_FONT, padx=15, pady=15, fg=PRIMARY_COLOR,
                           borderwidth=2, relief="groove")
config_frame.pack(fill="x", padx=20, pady=10, ipadx=5, ipady=5)

# Widgets de configuración
tk.Label(config_frame, text="Distribución:", bg=FRAME_COLOR, font=FONT, fg=PRIMARY_COLOR).grid(row=0, column=0, sticky="w", pady=5)
distribucion_var = ttk.Combobox(config_frame, values=["Uniforme", "Exponencial", "Normal"], 
                              state="readonly", font=FONT, width=18)
distribucion_var.grid(row=0, column=1, sticky="w", padx=5, pady=5)
distribucion_var.current(0)
distribucion_var.bind("<<ComboboxSelected>>", actualizar_parametros)

tk.Label(config_frame, text="Tamaño de muestra (1-1.000.000):", bg=FRAME_COLOR, font=FONT, fg=PRIMARY_COLOR).grid(row=1, column=0, sticky="w", pady=5)
entrada_muestra = ttk.Entry(config_frame, font=FONT, width=20)
entrada_muestra.grid(row=1, column=1, sticky="w", padx=5, pady=5)
entrada_muestra.insert(0, "1000")

# Parámetros dinámicos
label_param1 = tk.Label(config_frame, text="a:", bg=FRAME_COLOR, font=FONT, fg=PRIMARY_COLOR)
label_param1.grid(row=2, column=0, sticky="w", pady=5)
entrada_param1 = ttk.Entry(config_frame, font=FONT, width=20)
entrada_param1.grid(row=2, column=1, sticky="w", padx=5, pady=5)
entrada_param1.insert(0, "0")

label_param2 = tk.Label(config_frame, text="b:", bg=FRAME_COLOR, font=FONT, fg=PRIMARY_COLOR)
label_param2.grid(row=3, column=0, sticky="w", pady=5)
entrada_param2 = ttk.Entry(config_frame, font=FONT, width=20)
entrada_param2.grid(row=3, column=1, sticky="w", padx=5, pady=5)
entrada_param2.insert(0, "1")

tk.Label(config_frame, text="Número de intervalos (bins):", bg=FRAME_COLOR, font=FONT, fg=PRIMARY_COLOR).grid(row=4, column=0, sticky="w", pady=5)
bins_var = ttk.Combobox(config_frame, values=[5, 10, 15, 20, 25, 30], state="readonly", font=FONT, width=20)
bins_var.grid(row=4, column=1, sticky="w", padx=5, pady=5)
bins_var.current(1)

# Botón de ejecución
button_frame = tk.Frame(ventana, bg=BG_COLOR)
button_frame.pack(fill="x", padx=20, pady=5)
ejecutar_btn = tk.Button(button_frame, text="GENERAR DATOS", command=ejecutar, 
                        bg=BUTTON_COLOR, fg="white", font=("Segoe UI", 11, "bold"),
                        activebackground="#27ae60", activeforeground="white",
                        relief="raised", borderwidth=2, padx=15, pady=5)
ejecutar_btn.pack(pady=10)

# Frame de resultados
result_frame = tk.LabelFrame(ventana, text=" RESULTADOS ", bg=FRAME_COLOR, 
                           font=TITLE_FONT, padx=15, pady=15, fg="#2c3e50",
                           borderwidth=2, relief="groove")
result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20), ipadx=5, ipady=5)

# Estilos para pestañas
style = ttk.Style()
style.theme_use("clam")  # Importante para que se apliquen los colores personalizados

style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab",
                background=SECONDARY_COLOR,
                foreground=PRIMARY_COLOR,
                font=FONT,
                padding=[10, 5])
style.map("TNotebook.Tab",
          background=[("selected", PRIMARY_COLOR)],
          foreground=[("selected", "white"), ("!selected", PRIMARY_COLOR)])

style.layout("TNotebook.Tab", [
    ('Notebook.tab', {
        'sticky': 'nswe',
        'children': [
            ('Notebook.padding', {
                'side': 'top',
                'sticky': 'nswe',
                'children': [
                    ('Notebook.label', {'side': 'top', 'sticky': ''})
                ]
            })
        ]
    })
])

# Pestañas para organizar los resultados
notebook = ttk.Notebook(result_frame)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

# Pestaña de datos generados
tab_datos = ttk.Frame(notebook)
notebook.add(tab_datos, text="Datos Generados")

tk.Label(tab_datos, text="Valores generados:", font=HEADER_FONT, fg=PRIMARY_COLOR).pack(anchor="w", padx=5, pady=5)
text_datos = scrolledtext.ScrolledText(tab_datos, height=15, width=50, bg=TEXT_BG, font=FONT,
                                      wrap=tk.NONE, relief="solid", borderwidth=1)
text_datos.pack(fill="both", expand=True, padx=5, pady=5)

# Pestaña de tabla de frecuencias
tab_frecuencias = ttk.Frame(notebook)
notebook.add(tab_frecuencias, text="Tabla de Frecuencias")
tab_chi = ttk.Frame(notebook)
notebook.add(tab_chi, text="Chi-Cuadrado")

tk.Label(tab_frecuencias, text="Tabla de Frecuencias", 
         font=HEADER_FONT, fg="#2c3e50", bg=FRAME_COLOR).pack(anchor="w", padx=5, pady=(5, 0))
tk.Label(tab_frecuencias, text="Distribución de frecuencias:", 
         font=FONT, fg="#2c3e50", bg=FRAME_COLOR).pack(anchor="w", padx=5, pady=5)
tk.Label(tab_chi, text="Resultado Chi-Cuadrado", 
         font=HEADER_FONT, fg=PRIMARY_COLOR, bg=FRAME_COLOR).pack(anchor="w", padx=5, pady=(5, 0))

text_tabla = scrolledtext.ScrolledText(tab_frecuencias, height=15, width=50, bg=TEXT_BG, font=FONT,
                                     wrap=tk.NONE, relief="solid", borderwidth=1)
text_tabla.pack(fill="both", expand=True, padx=5, pady=5)
text_chi = scrolledtext.ScrolledText(tab_chi, height=10, width=60, bg=TEXT_BG, font=FONT,
                                     wrap=tk.WORD, relief="solid", borderwidth=1)
text_chi.pack(fill="both", expand=True, padx=5, pady=5)

# Configurar el grid para que sea responsivo
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(1, weight=1)

# Estilo para los widgets
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, font=FONT)
style.configure("TButton", font=FONT, background=BUTTON_COLOR)
style.configure("TCombobox", fieldbackground="white")
style.configure("TEntry", fieldbackground="white")

def iniciar_app():
    ventana.mainloop()