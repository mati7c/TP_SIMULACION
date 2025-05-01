def validar_tamano(tamano):
    try:
        n = int(tamano)
        if 1 <= n <= 1_000_000:
            return True, n
        return False, "El tamaño debe estar entre 1 y 1.000.000"
    except ValueError:
        return False, "Ingrese un número entero válido"

def validar_parametros(distribucion, parametros):
    try:
        if distribucion == "Uniforme":
            a = float(parametros["a"])
            b = float(parametros["b"])
            if a >= b:
                return False, "a debe ser menor que b"
        elif distribucion == "Normal":
            float(parametros["media"])
            float(parametros["desvio"])
        elif distribucion == "Exponencial":
            if float(parametros["lambda"]) <= 0:
                return False, "lambda debe ser mayor a 0"
        return True, ""
    except ValueError:
        return False, "Los parámetros deben ser numéricos"
