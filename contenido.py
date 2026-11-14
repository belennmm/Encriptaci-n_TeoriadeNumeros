"""Contenido académico en español, con fórmulas para Streamlit."""

introduccion_fundamentos = 'Para entender cómo funciona nuestro programa, primero necesitamos conocer algunos conceptos de teoría de números. Estos nos ayudan a trabajar con residuos, comprobar divisores y realizar las operaciones necesarias para encriptar y desencriptar mensajes.'

# Cada tema contiene bloques de texto y ecuaciones, en el orden de lectura.
fundamentos = [
    ('1. Divisibilidad', [
        ('texto', 'Un número es divisible entre otro cuando la división es exacta, es decir, cuando su residuo es cero.'),
        ('texto', '**Ejemplo:** 12 es divisible entre 3 porque 12 ÷ 3 = 4 y no sobra nada.'),
    ]),
    ('2. Algoritmo de la división', [
        ('texto', 'Cuando dividimos dos números enteros, obtenemos un cociente y un residuo. Estos valores cumplen con la siguiente fórmula:'),
        ('formula', r'a=dq+r'),
        ('texto', 'Donde a es el dividendo, d el divisor, q el cociente y r el residuo, que debe estar entre 0 y d − 1. El divisor d debe ser positivo.'),
        ('texto', '**Ejemplo:**'),
        ('formula', r'17=5(3)+2'),
        ('texto', 'El cociente es 3 y el residuo es 2.'),
    ]),
    ('3. Congruencias', [
        ('texto', 'Dos números son congruentes cuando dejan el mismo residuo al dividirse entre un mismo número.'),
        ('texto', '**Ejemplo:**'),
        ('formula', r'17\equiv5\pmod6'),
        ('texto', 'Esto sucede porque tanto 17 como 5 dejan residuo 5 al dividirse entre 6.'),
    ]),
    ('4. Operaciones modulares', [
        ('texto', 'La aritmética modular consiste en realizar operaciones y trabajar con el residuo de una división.'),
        ('texto', 'Podemos utilizar sumas, restas y multiplicaciones.'),
        ('texto', '**Ejemplo:**'),
        ('formula', r'(8+5)\bmod7=6'),
        ('texto', 'Esto significa que al dividir 13 entre 7 obtenemos un residuo de 6.'),
        ('texto', 'En nuestro programa utilizamos este tipo de operaciones para transformar los valores de los mensajes.'),
    ]),
    ('5. Números primos y factorización', [
        ('texto', 'Un número primo es aquel que tiene únicamente dos divisores positivos: 1 y él mismo.'),
        ('texto', 'Por ejemplo, 2, 3, 5 y 7 son primos.'),
        ('texto', 'La factorización consiste en descomponer un número en una multiplicación de números primos.'),
        ('texto', '**Ejemplo:**'),
        ('formula', r'60=2^2(3)(5)'),
    ]),
    ('6. Identificación y distribución de números primos', [
        ('texto', 'Para comprobar si un número es primo, podemos revisar si tiene divisores distintos de 1 y de sí mismo. Basta comprobar posibles divisores hasta su raíz cuadrada.'),
        ('texto', 'También existe la criba de Eratóstenes, que permite encontrar varios números primos eliminando los múltiplos de cada primo.'),
        ('texto', 'Los números primos son infinitos, aunque aparecen con menor frecuencia conforme aumentan los números.'),
        ('texto', 'Por ejemplo, entre 1 y 100 hay 25 números primos.'),
    ]),
    ('7. Máximo común divisor y mínimo común múltiplo', [
        ('texto', 'El máximo común divisor (MCD) es el número más grande que divide exactamente a dos números.'),
        ('texto', 'El mínimo común múltiplo (MCM) es el menor número positivo que es múltiplo de ambos.'),
        ('texto', '**Ejemplo:** Para 18 y 30:'),
        ('formula', r'\operatorname{MCD}(18,30)=6'),
        ('formula', r'\operatorname{MCM}(18,30)=90'),
        ('texto', 'En nuestro programa, el MCD es importante porque nos permite comprobar si un número tiene inverso modular, necesario para recuperar el mensaje original.'),
    ]),
    ('8. Algoritmo de Euclides', [
        ('texto', 'Es un procedimiento para calcular el MCD utilizando divisiones sucesivas.'),
        ('texto', '**Ejemplo:** Calcular el MCD de 18 y 12.'),
        ('formula', r'18=12(1)+6'),
        ('formula', r'12=6(2)+0'),
        ('texto', 'Como el último residuo diferente de cero es 6, tenemos:'),
        ('formula', r'\operatorname{MCD}(18,12)=6'),
        ('texto', 'Nuestro programa utiliza este algoritmo para comprobar si los valores elegidos permiten encriptar y desencriptar correctamente.'),
    ]),
]

teoremas = [
('Identidad de Bézout', 'Para enteros a y m no ambos nulos existen enteros x e y que expresan su MCD como combinación lineal.', r'ax+my=\operatorname{MCD}(a,m)', r'7(4)+27(-1)=1', 'Al reducir módulo 27, el coeficiente 4 es el inverso de 7.'),
('Euclides extendido y sustitución hacia atrás', 'Cada residuo se despeja de su división. Sustituimos hacia atrás hasta escribir el MCD en términos de los números originales. La tabla de coeficientes es otra forma equivalente de registrar el cálculo.', r'r_{i+1}=r_{i-1}-q_i r_i', r'27=7(3)+6,\quad7=6(1)+1;\quad1=7-6=7-(27-7(3))=4(7)-27', 'Los procedimientos de encriptación y desencriptación muestran estas sustituciones con los valores elegidos.'),
('Existencia del inverso modular', 'Para m > 1, a tiene inverso módulo m si y solo si MCD(a,m) = 1. No se puede cancelar ni dividir por un factor sin verificar esta condición.', r'\bigl(\exists x\in\mathbb Z:\ ax\equiv1\pmod m\bigr)\iff\operatorname{MCD}(a,m)=1', r'5(11)=55\equiv1\pmod{27}', 'En módulo 27, a = 3 no tiene inverso: los índices 0 y 9 producen el mismo índice cifrado para cualquier desplazamiento b.'),
('Reversibilidad del cifrado afín', 'Si a y m son coprimos, cada número entre 0 y m − 1 se transforma en un resultado distinto: el cifrado es una permutación de los residuos. Restar b y multiplicar por el inverso deshace la transformación.', r'a^{-1}(C-b)\equiv a^{-1}(aM+b-b)\equiv M\pmod m', r'C=(5(7)+8)\bmod27=16,\quad11(16-8)\bmod27=7', 'En módulo 27 se recuperan las letras y se conserva la distinción entre mayúsculas y minúsculas; los caracteres excluidos no cambian. En módulo 256 se recuperan todos los bytes y luego se reconstruye el texto con UTF-8.'),
]


teoremas.append(('Inverso en módulo 256',
 'Como los únicos factores primos de 256 son 2, un multiplicador tiene inverso exactamente cuando es impar. La demostración de reversibilidad es la misma que para módulo 27.',
 r'\operatorname{MCD}(a,256)=1\iff a\text{ es impar}',
 r'H\to72:\quad(5(72)+8)\bmod256=112,\quad205(112-8)\bmod256=72',
 'Los bytes recuperados se decodifican en conjunto mediante UTF-8. Una secuencia inválida genera un error; una secuencia válida no demuestra autenticidad ni seguridad moderna.'))
