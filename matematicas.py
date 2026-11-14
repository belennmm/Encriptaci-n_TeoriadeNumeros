"""Algoritmos elementales; los pasos se registran durante el cálculo."""

def validar_entero(numero):
    if type(numero) is not int:
        raise ValueError("Se necesita un número entero.")


def es_primo(numero):
    validar_entero(numero)
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def comprobar_primo(numero):
    """Devuelve cada divisor probado, incluido el primero que divide."""
    validar_entero(numero)
    pasos = []
    divisor = 2
    while numero >= 2 and divisor * divisor <= numero:
        pasos.append((numero, divisor, numero % divisor))
        if numero % divisor == 0:
            return False, pasos
        divisor += 1
    return numero >= 2, pasos


def calcular_mcd(numero1, numero2):
    validar_entero(numero1)
    validar_entero(numero2)
    numero1, numero2 = abs(numero1), abs(numero2)
    pasos = []
    while numero2:
        cociente, residuo = numero1 // numero2, numero1 % numero2
        pasos.append((numero1, numero2, cociente, residuo))
        numero1, numero2 = numero2, residuo
    return numero1, pasos


def euclides_extendido(numero1, numero2):
    validar_entero(numero1)
    validar_entero(numero2)
    anterior, actual = abs(numero1), abs(numero2)
    x_anterior, x = 1, 0
    y_anterior, y = 0, 1
    pasos = [(anterior, x_anterior, y_anterior), (actual, x, y)]
    while actual:
        cociente = anterior // actual
        anterior, actual = actual, anterior - cociente * actual
        x_anterior, x = x, x_anterior - cociente * x
        y_anterior, y = y, y_anterior - cociente * y
        pasos.append((actual, x, y))
    signo1 = -1 if numero1 < 0 else 1
    signo2 = -1 if numero2 < 0 else 1
    pasos = [(r, a * signo1, b * signo2) for r, a, b in pasos]
    return anterior, x_anterior * signo1, y_anterior * signo2, pasos


def buscar_inverso(numero, modulo):
    validar_entero(modulo)
    if modulo <= 1:
        raise ValueError("El módulo del inverso debe ser mayor que 1.")
    mcd, x, _, pasos = euclides_extendido(numero, modulo)
    if mcd != 1:
        raise ValueError(f"No existe inverso: el MCD es {mcd}, no 1.")
    return x % modulo, pasos


def potencia_modular(base, exponente, modulo):
    for numero in (base, exponente, modulo):
        validar_entero(numero)
    if exponente < 0 or modulo <= 0:
        raise ValueError("El exponente debe ser no negativo y el módulo positivo.")
    resultado, potencia = 1 % modulo, base % modulo
    pasos = []
    while exponente:
        anterior = resultado
        bit = exponente % 2
        if bit:
            resultado = resultado * potencia % modulo
        siguiente = potencia * potencia % modulo
        pasos.append(dict(exponente=exponente, bit=bit, potencia=potencia,
                          anterior=anterior, resultado=resultado, siguiente=siguiente))
        potencia = siguiente
        exponente //= 2
    return resultado, pasos


def sustituciones_euclides(numero, modulo):
    """Reconstruye Bézout sustituyendo residuos de las divisiones reales."""
    validar_entero(numero)
    validar_entero(modulo)
    if not 0 < numero < modulo:
        raise ValueError('Se necesita 0 < número < módulo.')
    mcd, divisiones = calcular_mcd(modulo, numero)
    despejes = {r: (a, b, q) for a, b, q, r in divisiones if r}
    terminos = {mcd: 1}
    pasos = []
    while any(r not in (numero, modulo) for r in terminos):
        residuo = min(r for r in terminos if r not in (numero, modulo))
        coeficiente = terminos.pop(residuo)
        a, b, cociente = despejes[residuo]
        terminos[a] = terminos.get(a, 0) + coeficiente
        terminos[b] = terminos.get(b, 0) - coeficiente * cociente
        terminos = {r: c for r, c in terminos.items() if c}
        pasos.append(dict(residuo=residuo, coeficiente=coeficiente,
                          numero=a, divisor=b, cociente=cociente,
                          terminos=dict(terminos)))
    return mcd, divisiones, pasos, terminos


def factorizar(numero):
    validar_entero(numero)
    if not 1 <= numero <= 1000000:
        raise ValueError('Ingresa un entero entre 1 y 1000000 para factorizar.')
    factores, pasos = {}, []
    divisor = 2
    while divisor * divisor <= numero:
        while numero % divisor == 0:
            pasos.append((numero, divisor, numero // divisor))
            factores[divisor] = factores.get(divisor, 0) + 1
            numero //= divisor
        divisor += 1
    if numero > 1:
        factores[numero] = factores.get(numero, 0) + 1
        pasos.append((numero, numero, 1))
    return factores, pasos


def criba_primos(limite=100):
    validar_entero(limite)
    if not 2 <= limite <= 10000:
        raise ValueError('El límite debe estar entre 2 y 10000.')
    disponibles = [True] * (limite + 1)
    disponibles[0] = disponibles[1] = False
    pasos = []
    divisor = 2
    while divisor * divisor <= limite:
        if disponibles[divisor]:
            eliminados = []
            for multiplo in range(divisor * divisor, limite + 1, divisor):
                if disponibles[multiplo]:
                    eliminados.append(multiplo)
                    disponibles[multiplo] = False
            pasos.append((divisor, eliminados))
        divisor += 1
    return [n for n in range(2, limite + 1) if disponibles[n]], pasos
