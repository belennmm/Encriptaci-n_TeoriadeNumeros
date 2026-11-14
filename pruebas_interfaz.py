"""Pruebas de navegación y del recorrido de la aplicación."""
import unittest
from streamlit.testing.v1 import AppTest

class PruebasInterfaz(unittest.TestCase):
    def test_recorrido(self):
        app = AppTest.from_file('app.py', default_timeout=30).run()
        for pagina in ('Fundamentos matemáticos', 'Teoremas y principios', 'Casos de uso', 'Encriptar y desencriptar'):
            app.sidebar.radio[0].set_value(pagina).run()
            self.assertFalse(app.exception)
        def pulsar(nombre):
            next(b for b in app.button if b.label == nombre).click().run()
            self.assertFalse(app.exception)
        app.radio[0].set_value('Alfabeto español (27 letras)').run()
        for texto in ('HOLA', '¡Hola, año 2026! Ññ áéíóú 😀'):
            app.text_area[0].set_value(texto).run()
            pulsar('Encriptar mensaje')
            if texto == 'HOLA':
                self.assertIn('PCJI', [c.value for c in app.code])
            pulsar('Desencriptar mensaje')
            self.assertIn(texto, [c.value for c in app.code])
            self.assertTrue(any('exactamente igual' in s.value for s in app.success))
        app.number_input[0].set_value(3).run()
        self.assertTrue(app.error)
        self.assertTrue(all(b.disabled for b in app.button))

    def test_herramientas_y_casos(self):
        app = AppTest.from_file('app.py', default_timeout=30).run()
        app.sidebar.radio[0].set_value('Fundamentos matemáticos').run()
        app.slider[0].set_value(4).run()
        app.number_input[0].set_value(360).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('360=' in ecuacion.value for ecuacion in app.latex))
        app.sidebar.radio[0].set_value('Casos de uso').run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.expander), 5)
        self.assertEqual([e.label.split('.')[0] for e in app.expander],
                         ['CU-01','CU-02','CU-03','CU-04','CU-05'])
        self.assertEqual(len(app.dataframe), 0)
        self.assertEqual(len(app.button), 0)
        for titulo in ('Objetivo','Datos de entrada','Pasos del usuario','Respuesta del programa','Resultado esperado'):
            self.assertEqual(sum(m.value == f'**{titulo}**' for m in app.markdown),5)
        self.assertEqual([c.value for c in app.code],
                         ['70 93 84 4d','HOLA','PCJI','70',
                          'No se puede usar a = 2: MCD(2, 256) = 2, no 1.'])

    def test_utf8(self):
        app = AppTest.from_file('app.py', default_timeout=30).run()
        app.sidebar.radio[0].set_value('Encriptar y desencriptar').run()
        self.assertEqual(app.radio[0].value,'Mensaje completo (UTF-8)')
        def pulsar(nombre):
            next(b for b in app.button if b.label == nombre).click().run()
            self.assertFalse(app.exception)
        for texto in ('H','HOLA','¡Hola, año 2026! Ññ 😀',''):
            app.text_area[0].set_value(texto).run()
            pulsar('Encriptar mensaje')
            if texto == 'H':
                self.assertIn('70',[c.value for c in app.code])
            if texto == 'HOLA':
                self.assertIn('70 93 84 4d',[c.value for c in app.code])
            pulsar('Desencriptar mensaje')
            self.assertIn(texto,[c.value for c in app.code])
            self.assertTrue(any('exactamente igual' in s.value for s in app.success))
        app.text_area[1].set_value('xx').run()
        pulsar('Desencriptar mensaje')
        self.assertTrue(app.error)
        app.radio[1].set_value('Decimal').run()
        app.text_area[1].set_value('112').run()
        pulsar('Desencriptar mensaje')
        self.assertIn('H',[c.value for c in app.code])
        app.number_input[0].set_value(4).run()
        self.assertTrue(app.error)
        self.assertTrue(all(b.disabled for b in app.button))

    def test_presentacion_compartida(self):
        app = AppTest.from_file('app.py', default_timeout=30).run()
        self.assertFalse(any('es-GT' in c.value for c in app.sidebar.caption))
        app.sidebar.radio[0].set_value('Casos de uso').run()
        compartidos = [e.label for e in app.expander if e.label.startswith('MCD e inverso:')]
        self.assertEqual(len(compartidos),0)
        self.assertEqual(len(compartidos),len(set(compartidos)))
        self.assertFalse(any('unittest' in c.value for c in app.code))
        app.sidebar.radio[0].set_value('Encriptar y desencriptar').run()
        for nombre in ('Encriptar mensaje','Desencriptar mensaje'):
            next(b for b in app.button if b.label == nombre).click().run()
        self.assertFalse(app.exception)
        compartidos = [e.label for e in app.expander if e.label.startswith('MCD e inverso:')]
        self.assertEqual(compartidos,['MCD e inverso: a = 5, m = 256'])
        self.assertEqual(len(app.dataframe),2)
        self.assertEqual(list(app.dataframe[0].value.columns),['Posición','Byte original','Operación modular','Byte cifrado'])

if __name__ == '__main__':
    unittest.main()
