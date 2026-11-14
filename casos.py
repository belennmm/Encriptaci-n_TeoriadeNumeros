"""Casos independientes que ejecutan los mismos algoritmos del laboratorio."""
from cifrado import cifrar_mensaje, descifrar_mensaje, preparar_clave, cifrar_utf8, descifrar_utf8
from matematicas import calcular_mcd


def ejecutar_casos():
    filas, detalles = [], []
    def agregar(nombre, entrada, esperado, obtenido, detalle):
        filas.append({'Caso': nombre, 'Datos de entrada': entrada,
                      'Resultado esperado': str(esperado), 'Resultado obtenido': str(obtenido),
                      'Estado': 'Comprobación correcta' if esperado == obtenido else 'Comprobación incorrecta'})
        detalles.append(detalle)
    cifrado, registro = cifrar_mensaje('HOLA')
    agregar('1. Encriptación', 'HOLA; a=5, b=8, m=27', 'PCJI', cifrado, registro)
    texto, registro = descifrar_mensaje('PCJI')
    agregar('2. Desencriptación', 'PCJI; a=5, b=8, m=27', 'HOLA', texto, registro)
    mcd, _ = calcular_mcd(5, 27)
    agregar('3. Multiplicador válido', 'a=5, m=27', 1, mcd, {'a': 5})
    try:
        preparar_clave(3, 8)
        rechazado = False
    except ValueError:
        rechazado = True
    agregar('4. Multiplicador sin inverso', 'a=3, b=8, m=27', 'Rechazado: no existe inverso', 'Rechazado: no existe inverso' if rechazado else 'Aceptado incorrectamente', {'a': 3})
    original = '¡Hola, año 2026! Ññ áéíóú ü'
    cifrado, registro = cifrar_mensaje(original)
    recuperado, vuelta = descifrar_mensaje(cifrado)
    agregar('5. Recuperación exacta', original + '; a=5, b=8', original, recuperado, (registro, vuelta))
    clave = preparar_clave(7, 8)
    agregar('6. Euclides extendido', 'a=7, m=27', 4, clave['inverso'], {'a': 7})
    cifrado, registro = cifrar_utf8('H')
    agregar('7. Byte UTF-8 de H', 'H; a=5, b=8, m=256', '70', cifrado.hex(), registro)
    texto, registro = descifrar_utf8(bytes([112]))
    agregar('8. Recuperación UTF-8', 'Hexadecimal 70; a=5, b=8, m=256', 'H', texto, registro)
    original = 'Contraseña: 12345; Ññ áéíóú ü'
    cifrado, registro = cifrar_utf8(original)
    texto, vuelta = descifrar_utf8(cifrado)
    agregar('9. Mensaje completo UTF-8', original + '; a=5, b=8', original, texto, (registro, vuelta))
    return filas, detalles

# Documentación de interacciones; las comprobaciones automáticas anteriores se conservan.
casos_uso = [
    {
        'codigo': 'CU-01',
        'nombre': 'Encriptar un mensaje completo',
        'objetivo': 'Encriptar un mensaje de texto utilizando la modalidad UTF-8 y operaciones de aritmética modular.',
        'entrada': ['Modalidad: Mensaje completo (UTF-8).', 'Mensaje: HOLA.', 'Multiplicador a = 5.', 'Desplazamiento b = 8.', 'Módulo m = 256.'],
        'pasos': ['Ingresa a «Encriptar y desencriptar» en el menú lateral.', 'Selecciona «Mensaje completo (UTF-8)».', 'Escribe HOLA en el campo «Mensaje original».', 'Ingresa a = 5 y b = 8.', 'Presiona «Encriptar mensaje».', 'Observa el mensaje cifrado y utiliza el botón de copiar del bloque si deseas guardarlo.'],
        'respuesta': 'El programa convierte el texto a bytes UTF-8, aplica la fórmula a cada byte y muestra el resultado en hexadecimal.',
        'formulas': [r'C=(aM+b)\bmod256'],
        'resultado': '70 93 84 4d',
        'explicacion': 'La secuencia puede copiarse para desencriptarla posteriormente con la misma modalidad y los mismos valores de a y b.',
    },
    {
        'codigo': 'CU-02',
        'nombre': 'Desencriptar un mensaje completo',
        'objetivo': 'Recuperar el mensaje original utilizando una secuencia cifrada y los parámetros correspondientes.',
        'entrada': ['Modalidad: Mensaje completo (UTF-8).', 'Formato: Hexadecimal.', 'Mensaje cifrado: 70 93 84 4d.', 'Multiplicador a = 5.', 'Desplazamiento b = 8.', 'Módulo m = 256.'],
        'pasos': ['Ingresa a «Encriptar y desencriptar» y selecciona «Mensaje completo (UTF-8)».', 'Selecciona «Hexadecimal» como formato de la secuencia cifrada.', 'Ingresa 70 93 84 4d en «Mensaje cifrado para desencriptar».', 'Establece a = 5 y b = 8.', 'Presiona «Desencriptar mensaje».', 'Consulta el mensaje recuperado.'],
        'respuesta': 'El programa calcula el inverso modular de a mediante Euclides extendido, aplica la operación inversa a los bytes cifrados y reconstruye el texto mediante UTF-8.',
        'formulas': [],
        'resultado': 'HOLA',
        'explicacion': 'El texto recuperado coincide exactamente con el original. Si el original fue encriptado en esta sesión con los mismos parámetros, el programa también muestra la verificación de igualdad.',
    },
    {
        'codigo': 'CU-03',
        'nombre': 'Encriptar con el alfabeto español',
        'objetivo': 'Mostrar cómo se utilizan los índices de las letras del alfabeto español para encriptar un mensaje mediante congruencias.',
        'entrada': ['Modalidad: Alfabeto español (27 letras).', 'Mensaje: HOLA.', 'Multiplicador a = 5.', 'Desplazamiento b = 8.', 'Módulo m = 27.'],
        'pasos': ['Ingresa a «Encriptar y desencriptar».', 'Selecciona «Alfabeto español (27 letras)».', 'Escribe HOLA.', 'Establece a = 5 y b = 8.', 'Presiona «Encriptar mensaje».', 'Consulta el mensaje cifrado.'],
        'respuesta': 'El programa convierte cada letra a un número entre 0 y 26, aplica la operación modular y transforma el resultado nuevamente en una letra.',
        'formulas': [],
        'resultado': 'PCJI',
        'explicacion': 'En esta modalidad se conservan mayúsculas y minúsculas. Los caracteres que no pertenecen al alfabeto de 27 letras permanecen sin modificar.',
    },
    {
        'codigo': 'CU-04',
        'nombre': 'Consultar el procedimiento matemático',
        'objetivo': 'Observar las operaciones de teoría de números que utiliza el programa para encriptar.',
        'entrada': ['Modalidad: Mensaje completo (UTF-8).', 'Mensaje: H.', 'Multiplicador a = 5.', 'Desplazamiento b = 8.', 'Módulo m = 256.'],
        'pasos': ['Ingresa a «Encriptar y desencriptar» y selecciona «Mensaje completo (UTF-8)».', 'Escribe H y establece a = 5 y b = 8.', 'Presiona «Encriptar mensaje».', 'Abre «Procedimiento completo de encriptación».', 'Selecciona «Posición 1» en «Byte que deseas analizar».', 'Consulta las operaciones del byte seleccionado.', 'Para revisar Euclides y el inverso, abre «MCD e inverso: a = 5, m = 256» al final de esa sección.'],
        'respuesta': 'El programa muestra la conversión a bytes y desarrolla la operación modular. El cálculo compartido del MCD y del inverso está disponible en su propio desplegable.',
        'formulas': [r'H\to72', r'C=(5(72)+8)\bmod256', r'C=368\bmod256=112'],
        'resultado': '70',
        'explicacion': 'H corresponde al byte 72. El byte cifrado 112 se representa como 70 en hexadecimal. También se puede consultar que MCD(5, 256) = 1 y que el inverso de 5 es 205.',
    },
    {
        'codigo': 'CU-05',
        'nombre': 'Validar un multiplicador incorrecto',
        'objetivo': 'Comprobar que el programa detecta valores que no permiten recuperar correctamente un mensaje.',
        'entrada': ['Modalidad: Mensaje completo (UTF-8).', 'Mensaje: HOLA.', 'Multiplicador a = 2.', 'Desplazamiento b = 8.', 'Módulo m = 256.'],
        'pasos': ['Ingresa a «Encriptar y desencriptar» y selecciona «Mensaje completo (UTF-8)».', 'Escribe HOLA.', 'Establece a = 2 y b = 8.', 'Observa la validación del multiplicador y los botones de operación.'],
        'respuesta': 'El campo permite ingresar a = 2, pero el programa detecta que su MCD con 256 no es 1. Muestra un error y deshabilita los botones «Encriptar mensaje» y «Desencriptar mensaje».',
        'formulas': [r'\operatorname{MCD}(2,256)=2'],
        'resultado': 'No se puede usar a = 2: MCD(2, 256) = 2, no 1.',
        'explicacion': 'No se realiza la operación porque no existe inverso modular. Se debe elegir un multiplicador coprimo con 256; en esta modalidad, un número impar.',
    },
]
