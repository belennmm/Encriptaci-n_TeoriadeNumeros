"""Pruebas independientes del cifrado y sus trazas."""
import unittest
from cifrado import *
from matematicas import *

class PruebasCifrado(unittest.TestCase):
    def test_hola(self):
        self.assertEqual(cifrar_mensaje('HOLA')[0], 'PCJI')
        self.assertEqual(descifrar_mensaje('PCJI')[0], 'HOLA')
        self.assertEqual(preparar_clave(5, 8)['inverso'], 11)

    def test_claves_invalidas(self):
        for a in (0, 3, 6, 9, 12, 15, 18, 21, 24, -1, 27, 1.5, True):
            with self.assertRaises(ValueError):
                preparar_clave(a, 8)
        for b in (-1, 27, '8', False):
            with self.assertRaises(ValueError):
                preparar_clave(5, b)
        with self.assertRaises(ValueError):
            preparar_clave(5, 8, 26)

    def test_texto_exacto(self):
        for texto in ('', '¡Hola, año 2026!', 'Ññ ÁÉÍÓÚ áéíóú ü 😀', '  A\nB\t!\x00', 'n\u0303 e\u0301', alfabeto + alfabeto.lower()):
            cifrado, _ = cifrar_mensaje(texto)
            self.assertEqual(descifrar_mensaje(cifrado)[0], texto)
        self.assertEqual(cifrar_mensaje(' áéíóú ü 123!? 😀')[0], ' áéíóú ü 123!? 😀')

    def test_todas_las_claves(self):
        for a in range(27):
            if calcular_mcd(a, 27)[0] != 1:
                continue
            for b in range(27):
                texto = alfabeto + alfabeto.lower() + ' ¡á! 2026'
                cifrado, _ = cifrar_mensaje(texto, a, b)
                self.assertEqual(len(set(cifrado[:27])), 27)
                self.assertEqual(descifrar_mensaje(cifrado, a, b)[0], texto)

    def test_trazas(self):
        for funcion in (cifrar_mensaje, descifrar_mensaje):
            resultado, registro = funcion('HOLA Ññ á!')
            clave = registro['clave']
            for numero, divisor, cociente, residuo in clave['pasos_mcd']:
                self.assertEqual(numero, divisor*cociente + residuo)
            for residuo, x, y in clave['pasos_inverso']:
                self.assertEqual(residuo, 5*x + 27*y)
            for paso in registro['pasos']:
                if paso['conservado']:
                    self.assertEqual(paso['letra'], paso['salida'])
                else:
                    esperado = 11*(paso['valor']-8) if registro['descifrar'] else 5*paso['valor']+8
                    self.assertEqual(paso['operacion'], esperado)
                    self.assertEqual(esperado, 27*paso['cociente'] + paso['residuo'])
                    self.assertEqual(paso['salida'].upper(), alfabeto[paso['residuo']])
            self.assertEqual(resultado, ''.join(p['salida'] for p in registro['pasos']))

    def test_herramientas_conservadas(self):
        self.assertTrue(es_primo(53))
        self.assertFalse(comprobar_primo(91)[0])
        self.assertEqual(calcular_mcd(18,30)[0],6)
        self.assertEqual(buscar_inverso(5,27)[0],11)
        self.assertEqual(potencia_modular(3,4,27)[0],0)

class PruebasAmpliacion(unittest.TestCase):
    def test_sustituciones(self):
        for a in range(1, 27):
            mcd, divisiones, pasos, terminos = sustituciones_euclides(a, 27)
            anterior = {mcd: 1}
            for paso in pasos:
                r, c = paso['residuo'], paso['coeficiente']
                self.assertEqual(anterior[r], c)
                self.assertEqual(r, paso['numero'] - paso['divisor'] * paso['cociente'])
                esperado = dict(anterior)
                esperado.pop(r)
                for numero, coeficiente in ((paso['numero'], c), (paso['divisor'], -c*paso['cociente'])):
                    esperado[numero] = esperado.get(numero, 0) + coeficiente
                esperado = {r: c for r, c in esperado.items() if c}
                self.assertEqual(esperado, paso['terminos'])
                self.assertEqual(sum(r*c for r,c in esperado.items()), mcd)
                anterior = esperado
            self.assertEqual(terminos, anterior)
            self.assertTrue(set(terminos) <= {a,27})
            if mcd == 1:
                self.assertEqual(terminos.get(a,0) % 27, buscar_inverso(a,27)[0])
        self.assertEqual(buscar_inverso(7,27)[0],4)

    def test_criba(self):
        primos, pasos = criba_primos(100)
        self.assertEqual(primos, [n for n in range(2,101) if es_primo(n)])
        self.assertEqual(len(primos),25)
        eliminados = set()
        for divisor, numeros in pasos:
            for numero in numeros:
                self.assertEqual(numero % divisor,0)
                self.assertNotIn(numero, eliminados)
                eliminados.add(numero)
        self.assertEqual(set(range(2,101)) - eliminados, set(primos))

    def test_factorizacion(self):
        for numero in (1,2,27,60,97,360,1000000):
            factores, pasos = factorizar(numero)
            producto = 1
            for primo, exponente in factores.items():
                self.assertTrue(es_primo(primo))
                producto *= primo ** exponente
            self.assertEqual(producto,numero)
            restante = numero
            for valor, divisor, cociente in pasos:
                self.assertEqual(valor,restante)
                self.assertEqual(valor, divisor*cociente)
                restante = cociente
            self.assertEqual(restante,1)

    def test_casos(self):
        from casos import ejecutar_casos
        filas, detalles = ejecutar_casos()
        self.assertEqual(len(filas),9)
        self.assertEqual(len(detalles),9)
        self.assertTrue(all(f['Estado'] == 'Comprobación correcta' for f in filas))

class PruebasUTF8(unittest.TestCase):
    def test_ejemplo_h(self):
        cifrado, registro = cifrar_utf8('H')
        self.assertEqual(cifrado, bytes([112]))
        self.assertEqual(cifrado.hex(), '70')
        self.assertEqual(registro['pasos'][0]['operacion'],368)
        texto, registro = descifrar_utf8(cifrado)
        self.assertEqual(texto,'H')
        self.assertEqual(registro['clave']['inverso'],205)
        self.assertEqual(registro['pasos'][0]['operacion'],21320)

    def test_textos(self):
        for texto in ('HOLA', 'Hola, mundo', '¡Hola, año 2026!', 'Matemática Discreta',
                      'Ññ áéíóú ü', 'Contraseña: 12345', 'Mensaje con 😀', '',
                      '  \n\t\x00', 'e\u0301', 'ñ'*2000):
            cifrado, registro = cifrar_utf8(texto)
            self.assertEqual(len(cifrado),len(texto.encode('utf-8')))
            self.assertEqual(len(registro['pasos']),len(cifrado))
            self.assertEqual(descifrar_utf8(cifrado)[0],texto)

    def test_residuos_y_claves(self):
        originales = bytes(range(256))
        for a in range(1,256,2):
            for b in (0,8,255):
                cifrado, registro = cifrar_bytes(originales,a,b)
                self.assertEqual(len(set(cifrado)),256)
                self.assertEqual(descifrar_bytes(cifrado,a,b)[0],originales)
                self.assertEqual(registro['clave']['inverso']*a % 256,1)
                mcd, _, _, terminos = sustituciones_euclides(a,256)
                self.assertEqual(mcd,1)
                self.assertEqual(sum(r*c for r,c in terminos.items()),1)

    def test_errores(self):
        for a in range(0,256,2):
            with self.assertRaises(ValueError): preparar_clave(a,8,256)
        for b in (-1,256,1.5,True):
            with self.assertRaises(ValueError): preparar_clave(5,b,256)
        for valores in ([-1],[256],[1.5],[True],'70',None):
            with self.assertRaises(ValueError): descifrar_bytes(valores)
        for texto in ('0','gg','0x70','70,71'):
            with self.assertRaises(ValueError): leer_bytes(texto)
        for texto in ('256','-1','1.5','1,,2'):
            with self.assertRaises(ValueError): leer_bytes(texto,'Decimal')
        cifrado, _ = cifrar_bytes([255])
        with self.assertRaisesRegex(ValueError,'UTF-8 válido'):
            descifrar_utf8(cifrado)

    def test_formatos(self):
        for formato,texto in (('Hexadecimal','70 FF 00'),('Decimal','112, 255, 0'),('Decimal','112 255 0')):
            self.assertEqual(leer_bytes(texto,formato),bytes([112,255,0]))
        self.assertEqual(leer_bytes(''),b'')
        self.assertEqual(leer_bytes('','Decimal'),b'')

    def test_trazas_utf8(self):
        cifrado, registro = cifrar_utf8('¡Ññ!')
        texto, vuelta = descifrar_utf8(cifrado)
        for datos in (registro,vuelta):
            for paso in datos['pasos']:
                valor = paso['valor']
                esperado = 205*(valor-8) if datos['descifrar'] else 5*valor+8
                self.assertEqual(paso['operacion'],esperado)
                self.assertEqual(esperado,256*paso['cociente']+paso['residuo'])
                self.assertTrue(0 <= paso['residuo'] <= 255)

if __name__ == '__main__':
    unittest.main()
