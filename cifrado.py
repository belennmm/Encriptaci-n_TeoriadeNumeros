"""Cifrado afín educativo sobre las 27 letras españolas."""
from matematicas import validar_entero, calcular_mcd, buscar_inverso

alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'


def preparar_clave(a, b, m=27):
    for numero in (a, b, m):
        validar_entero(numero)
    if m not in (27, 256):
        raise ValueError('El módulo debe ser 27 (alfabeto) o 256 (UTF-8).')
    if not 0 <= a < m or not 0 <= b < m:
        raise ValueError(f'a y b deben ser enteros entre 0 y {m - 1}.')
    mcd, pasos_mcd = calcular_mcd(m, a)
    if mcd != 1:
        raise ValueError(f'No se puede usar a = {a}: MCD({a}, {m}) = {mcd}, no 1.')
    inverso, pasos_inverso = buscar_inverso(a, m)
    return dict(a=a, b=b, m=m, inverso=inverso,
                pasos_mcd=pasos_mcd, pasos_inverso=pasos_inverso)


def transformar_mensaje(mensaje, a, b, descifrar=False):
    if not isinstance(mensaje, str):
        raise ValueError('El mensaje debe ser texto.')
    clave = preparar_clave(a, b)
    resultado, pasos = [], []
    minusculas = alfabeto.lower()
    for letra in mensaje:
        letras = alfabeto if letra in alfabeto else minusculas
        if letra not in letras:
            resultado.append(letra)
            pasos.append(dict(letra=letra, salida=letra, conservado=True))
            continue
        valor = letras.index(letra)
        operacion = clave['inverso'] * (valor - b) if descifrar else a * valor + b
        residuo = operacion % clave['m']
        salida = letras[residuo]
        resultado.append(salida)
        pasos.append(dict(letra=letra, valor=valor, operacion=operacion,
                          cociente=operacion // clave['m'], residuo=residuo,
                          salida=salida, conservado=False))
    return ''.join(resultado), dict(clave=clave, pasos=pasos,
                                   entrada=mensaje, descifrar=descifrar)


def cifrar_mensaje(mensaje, a=5, b=8):
    return transformar_mensaje(mensaje, a, b)


def descifrar_mensaje(mensaje, a=5, b=8):
    return transformar_mensaje(mensaje, a, b, descifrar=True)


def validar_bytes(valores):
    if not isinstance(valores, (bytes, bytearray, list, tuple)):
        raise ValueError('Se necesita una secuencia de bytes enteros.')
    if any(type(valor) is not int or not 0 <= valor <= 255 for valor in valores):
        raise ValueError('Cada byte debe ser un entero entre 0 y 255.')


def transformar_bytes(valores, a, b, descifrar=False):
    validar_bytes(valores)
    clave = preparar_clave(a, b, 256)
    resultado, pasos = [], []
    for valor in valores:
        producto = clave['inverso'] * (valor - b) if descifrar else a * valor
        operacion = producto if descifrar else producto + b
        residuo = operacion % 256
        resultado.append(residuo)
        pasos.append(dict(valor=valor, producto=producto, operacion=operacion,
                          cociente=operacion // 256, residuo=residuo))
    return bytes(resultado), dict(clave=clave, entrada=list(valores), pasos=pasos,
                                 descifrar=descifrar, modo='UTF-8')


def cifrar_bytes(valores, a=5, b=8):
    return transformar_bytes(valores, a, b)


def descifrar_bytes(valores, a=5, b=8):
    return transformar_bytes(valores, a, b, descifrar=True)


def cifrar_utf8(mensaje, a=5, b=8):
    if not isinstance(mensaje, str):
        raise ValueError('El mensaje debe ser texto.')
    try:
        originales = mensaje.encode('utf-8')
    except UnicodeEncodeError as error:
        raise ValueError('El texto contiene caracteres Unicode que no se pueden codificar en UTF-8.') from error
    resultado, registro = cifrar_bytes(originales, a, b)
    registro['texto'] = mensaje
    return resultado, registro


def descifrar_utf8(valores, a=5, b=8):
    originales, registro = descifrar_bytes(valores, a, b)
    try:
        texto = originales.decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Los bytes recuperados no forman texto UTF-8 válido. Revisa el cifrado y los parámetros a y b.') from error
    registro['texto'] = texto
    return texto, registro


def leer_bytes(texto, formato='Hexadecimal'):
    if not isinstance(texto, str):
        raise ValueError('Ingresa la secuencia cifrada como texto.')
    if formato == 'Hexadecimal':
        limpio = ''.join(texto.split())
        if len(limpio) % 2 or any(letra not in '0123456789abcdefABCDEF' for letra in limpio):
            raise ValueError('Hexadecimal inválido: usa dos dígitos por byte, con espacios opcionales.')
        return bytes.fromhex(limpio)
    if formato != 'Decimal':
        raise ValueError('Selecciona Hexadecimal o Decimal.')
    if not texto.strip():
        return b''
    partes = texto.split(',') if ',' in texto else texto.split()
    try:
        valores = [int(parte.strip()) for parte in partes]
    except ValueError as error:
        raise ValueError('Usa enteros decimales separados por comas o espacios.') from error
    validar_bytes(valores)
    return bytes(valores)
