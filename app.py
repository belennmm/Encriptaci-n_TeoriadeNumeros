"""Interfaz educativa local: python -m streamlit run app.py."""
import streamlit as st
from contenido import fundamentos, teoremas, introduccion_fundamentos
from cifrado import (alfabeto, preparar_clave, cifrar_mensaje, descifrar_mensaje,
                     cifrar_utf8, descifrar_utf8, leer_bytes)
from matematicas import comprobar_primo, calcular_mcd, sustituciones_euclides, criba_primos, factorizar
from casos import casos_uso

st.set_page_config(page_title='Encriptación usando teoría de números', layout='wide')
st.markdown('''<style>.stApp{background:#f7f8fc;color:#18283c}.block-container{max-width:1120px;padding-top:2.5rem}h1,h2,h3{color:#244b65}[data-testid="stSidebar"]{background:#eaf0f5}</style>''', unsafe_allow_html=True)


def mostrar_fichas(fichas):
    for nombre, definicion, formula, ejemplo, aplicacion in fichas:
        with st.expander(nombre):
            st.write(definicion)
            st.latex(formula)
            st.markdown('**Ejemplo resuelto**')
            st.latex(ejemplo)
            st.info('Aplicación en la encriptación: ' + aplicacion)


def mostrar_procedimiento(registro, nombre):
    if registro.get('modo') == 'UTF-8':
        mostrar_bytes(registro, nombre)
        return
    clave = registro['clave']
    a, b, m, inverso = (clave[campo] for campo in ('a', 'b', 'm', 'inverso'))
    with st.expander('Procedimiento completo de ' + nombre):
        st.write('Texto utilizado:', registro['entrada'])
        st.latex(fr'a={a},\quad b={b},\quad m={m}')
        solicitar_inverso(a, m)
        st.markdown('**Conversión y operaciones por carácter**')
        for indice, paso in enumerate(registro['pasos'], 1):
            st.write(f'Posición {indice}: {paso["letra"]!r} → {paso["salida"]!r}')
            if paso['conservado']:
                st.caption('Fuera del alfabeto: se conserva exactamente, sin operación modular.')
                continue
            valor, residuo = paso['valor'], paso['residuo']
            if registro['descifrar']:
                st.latex(fr'M={inverso}({valor}-{b})\bmod{m}={residuo}')
            else:
                st.latex(fr'C=({a}({valor})+{b})\bmod{m}={residuo}')
            st.latex(fr'{paso["operacion"]}={m}({paso["cociente"]})+{residuo}')
            st.caption(f'Índice de entrada: {valor}; índice de salida: {residuo}; letra: {paso["salida"]}.')
        if not registro['pasos']:
            st.write('El mensaje vacío no requiere operaciones.')


def mostrar_bytes(registro, nombre):
    clave = registro['clave']
    a, b, inverso = (clave[c] for c in ('a', 'b', 'inverso'))
    with st.expander('Procedimiento completo de ' + nombre):
        st.write('Texto recuperado' if registro['descifrar'] else 'Texto original', registro['texto'])
        st.latex(fr'a={a},\quad b={b},\quad m=256')
        solicitar_inverso(a, 256)
        st.dataframe([{'Posición': i+1, ('Byte cifrado' if registro['descifrar'] else 'Byte original'): p['valor'],
                   'Operación modular': f"{inverso} × ({p['valor']} − {b}) mod 256" if registro['descifrar'] else f"({a} × {p['valor']} + {b}) mod 256",
                   'Byte recuperado' if registro['descifrar'] else 'Byte cifrado': p['residuo']}
                  for i, p in enumerate(registro['pasos'])], hide_index=True, width='stretch', height=300)
        if registro['pasos']:
            indice = st.selectbox('Byte que deseas analizar', range(len(registro['pasos'])),
                                  format_func=lambda i: f'Posición {i+1}', key='byte_' + nombre)
            paso = registro['pasos'][indice]
            valor = paso['valor']
            with st.expander('Operaciones del byte seleccionado', expanded=True):
                if registro['descifrar']:
                    st.latex(fr'{valor}-{b}={valor-b}')
                    st.latex(fr'{inverso}({valor-b})={paso["producto"]}')
                else:
                    st.latex(fr'{a}({valor})={paso["producto"]}')
                    st.latex(fr'{paso["producto"]}+{b}={paso["operacion"]}')
                st.latex(fr'{paso["operacion"]}=256({paso["cociente"]})+{paso["residuo"]}')
                st.latex(fr'{paso["operacion"]}\bmod256={paso["residuo"]}')
        else:
            st.write('Mensaje vacío: cero bytes, no hay operaciones por byte.')
        st.write('Después de recuperar todos los bytes, se convierten juntos al texto original mediante UTF-8.' if registro['descifrar'] else 'Cada carácter puede ocupar varios bytes UTF-8. Se aplica la fórmula a todos los bytes, aunque alguno puede mantener su valor.')


# Se reinicia en cada actualización para compartir los procedimientos visibles.
inversos_solicitados = set()


def solicitar_inverso(a, m):
    inversos_solicitados.add((a, m))
    st.caption(f'Las divisiones y el cálculo del inverso están al final de esta sección, en «MCD e inverso: a = {a}, m = {m}». Se comparten entre operaciones con los mismos valores.')


def mostrar_inverso(a, m):
    mcd, divisiones, pasos, terminos = sustituciones_euclides(a, m)
    st.markdown('**1. Divisiones de Euclides y MCD**')
    for numero, divisor, cociente, residuo in divisiones:
        st.latex(fr'{numero}={divisor}({cociente})+{residuo}')
    st.latex(fr'\operatorname{{MCD}}({a},{m})={mcd}')
    st.markdown('**2. Despejes de los residuos no nulos**')
    for numero, divisor, cociente, residuo in divisiones:
        if residuo:
            st.latex(fr'{residuo}={numero}-{divisor}({cociente})')
    st.markdown('**3. Sustituciones hacia atrás**')
    expresion = str(mcd)
    for paso in pasos:
        residuo = paso['residuo']
        reemplazo = fr"({paso['numero']}-{paso['divisor']}({paso['cociente']}))"
        # Se reemplaza un residuo de la expresión anterior por su despeje.
        if expresion == str(mcd):
            expandida = reemplazo
        else:
            expandida = ' + '.join(fr"({c})" + (reemplazo if r == residuo else fr'({r})') for r, c in anteriores.items())
        st.latex(fr'{mcd}={expandida}')
        expresion = ' + '.join(fr'({c})({r})' for r, c in paso['terminos'].items())
        st.latex(fr'{mcd}={expresion}')
        anteriores = paso['terminos']
    if not pasos:
        st.write('El MCD ya es uno de los números originales; no se requieren sustituciones.')
    st.markdown('**4. Identidad de Bézout**')
    x, y = terminos.get(a, 0), terminos.get(m, 0)
    st.latex(fr'{mcd}=({x})({a})+({y})({m})')
    if mcd == 1:
        inverso = x % m
        st.markdown('**5. Inverso y comprobación**')
        st.latex(fr'a^{{-1}}={x}\bmod{m}={inverso}')
        st.latex(fr'{a}({inverso})\bmod{m}={a*inverso%m}')
        with st.expander('Detalle adicional: tabla de coeficientes'):
            clave = preparar_clave(a, 0, m)
            st.table([{'Residuo': r, 'Coeficiente de a': u, 'Coeficiente de m': v} for r, u, v in clave['pasos_inverso']])
    else:
        st.write('El MCD no es 1: no existe inverso modular y el multiplicador se rechaza.')


def mostrar_herramientas():
    with st.expander('Criba de Eratóstenes: del 2 al 100'):
        primos, pasos = criba_primos(100)
        etapa = st.slider('Etapa de eliminación', 0, len(pasos), 0)
        eliminados = {n for _, numeros in pasos[:etapa] for n in numeros}
        for primo, numeros in pasos[:etapa]:
            st.write(f'Primo {primo}: se eliminan sus múltiplos todavía disponibles:', numeros)
        st.table([{'Número': n, 'Estado': 'Eliminado' if n in eliminados else ('Primo' if etapa == len(pasos) else 'Disponible')} for n in range(2, 101)])
        if etapa == len(pasos):
            st.write('Primos encontrados:', primos)
            st.write('Cantidad exacta: 25. Aproximación 100/ln(100): 21.71; no es una cuenta exacta.')
    with st.expander('Factorización prima paso a paso'):
        numero = int(st.number_input('Entero para factorizar', min_value=1, max_value=1000000, value=60))
        factores, pasos = factorizar(numero)
        for valor, divisor, cociente in pasos:
            st.latex(fr'{valor}={divisor}({cociente})')
        if factores:
            producto = r'\cdot'.join(fr'{primo}^{{{exponente}}}' for primo, exponente in factores.items())
            st.latex(fr'{numero}={producto}')
        else:
            st.write('1 no tiene factores primos: corresponde al producto vacío.')


st.sidebar.title('Encriptación usando teoría de números')
pagina = st.sidebar.radio('Secciones', ['Introducción a la encriptación', 'Fundamentos matemáticos', 'Teoremas y principios', 'Encriptar y desencriptar', 'Casos de uso'])
if pagina == 'Introducción a la encriptación':
    st.title('Encriptación usando teoría de números')
    st.write('El objetivo de este programa es encriptar y recuperar mensajes usando operaciones de teoría de números. Con el cifrado afín podemos ver cómo la aritmética modular, el MCD y los inversos convierten un mensaje en otro y permiten regresar al original.')
    st.info('Mensaje original → Encriptación → Mensaje cifrado → Desencriptación → Mensaje recuperado')
    st.subheader('Dos modos para explorar el mismo método')
    st.markdown('**Alfabeto español (módulo 27).** Cada una de las 27 letras, incluida la Ñ, tiene un número de 0 a 26. Se conservan mayúsculas y minúsculas. Los espacios, las vocales con tilde, los números y otros símbolos quedan visibles. Este modo ayuda a explicar el cálculo letra por letra.')
    st.markdown('**Mensaje completo mediante UTF-8 (módulo 256).** El texto se convierte en bytes, números entre 0 y 255. La fórmula se aplica a todos ellos, incluidos los que representan espacios y caracteres especiales. El resultado se muestra en hexadecimal, una forma de escribir los bytes con dos dígitos. Este es el modo recomendado.')
    st.subheader('¿Por qué elegimos hacerlo de esta forma?')
    st.write('Elegimos el cifrado afín porque permite aplicar directamente varios temas de teoría de números que estudiamos en clase, como las congruencias, el MCD y el algoritmo de Euclides. Además, podemos programar cada operación por nuestra cuenta y comprobar matemáticamente cómo se encripta y recupera un mensaje.')
    st.subheader('Cómo se transforma y se recupera el mensaje')
    st.latex(r'C=(aM+b)\bmod m,\qquad M=a^{-1}(C-b)\bmod m')
    st.write('Donde M es el valor original y C el valor cifrado. Los números a y b se utilizan para transformar el mensaje, mientras que m es el módulo, que puede ser 27 o 256 según el modo seleccionado.')
    st.write('Para poder recuperar el mensaje, es necesario que MCD(a, m) = 1. Esto permite encontrar el inverso modular de a y realizar la operación contraria.')
    st.write('Por ejemplo, con a = 5 y b = 8, la palabra HOLA se convierte en PCJI en el modo alfabeto. En el modo UTF-8, la letra H tiene un valor de 72 y se transforma en 112, que se representa como 70 en hexadecimal.')
    st.write('El programa permite consultar las operaciones paso a paso para comprender cómo se obtiene cada resultado.')

    st.caption('Referencia: Kenneth H. Rosen, Discrete Mathematics and Its Applications, 8.ª edición.')
elif pagina == 'Fundamentos matemáticos':
    st.title(pagina)
    st.write(introduccion_fundamentos)
    for titulo, bloques in fundamentos:
        with st.expander(titulo):
            for tipo, contenido in bloques:
                if tipo == 'formula':
                    st.latex(contenido)
                else:
                    st.markdown(contenido)
    mostrar_herramientas()
elif pagina == 'Teoremas y principios':
    st.title('Principios matemáticos de la encriptación')
    mostrar_fichas(teoremas)
elif pagina == 'Encriptar y desencriptar':
    st.title('Encriptación y desencriptación')
    modo = st.radio('Modalidad', ['Mensaje completo (UTF-8)', 'Alfabeto español (27 letras)'])
    utf8 = modo == 'Mensaje completo (UTF-8)'
    modulo = 256 if utf8 else 27
    st.info('Recomendado: UTF-8 transforma todos los bytes del mensaje, incluidos espacios, números y caracteres especiales. El modo de 27 letras ayuda a explicar los índices de las letras.')
    if utf8:
        st.write('Se utiliza módulo 256. Como 256 = 2⁸, MCD(a, 256) = 1 si y solo si a es impar. La salida cifrada se muestra como hexadecimal, nunca como texto UTF-8.')
    else:
        st.write('Se encriptan las 27 letras conservando mayúsculas y minúsculas. Los espacios, números, vocales con tilde y otros símbolos se conservan sin modificar. Esta es una limitación del modo educativo de alfabeto.')
        with st.expander('Alfabeto español e índices'):
            st.table([{'Letra': letra, 'Valor': i} for i, letra in enumerate(alfabeto)])
    izquierda, derecha = st.columns(2)
    a = int(izquierda.number_input(f'Multiplicador a (0–{modulo-1})', min_value=0, max_value=modulo-1, value=5, step=1, key=f'a_{modulo}'))
    b = int(derecha.number_input(f'Desplazamiento b (0–{modulo-1})', min_value=0, max_value=modulo-1, value=8, step=1, key=f'b_{modulo}'))
    try:
        clave = preparar_clave(a, b, modulo)
        st.success(f'MCD({a}, {modulo}) = 1. Inverso de {a}: {clave["inverso"]}.')
    except ValueError as error:
        st.error(str(error))
        clave = None
    st.caption('Cada resultado conserva su modo y parámetros; para generar otro resultado, presiona el botón correspondiente.')
    mensaje = st.text_area('Mensaje original', value='HOLA', max_chars=2000)
    cifrar = cifrar_utf8 if utf8 else cifrar_mensaje
    descifrar = descifrar_utf8 if utf8 else descifrar_mensaje
    salida_clave, vuelta_clave, entrada_clave = (f'{nombre}_{modulo}' for nombre in ('cifrado', 'descifrado', 'entrada'))
    if st.button('Encriptar mensaje', type='primary', disabled=clave is None):
        try:
            resultado, registro = cifrar(mensaje, a, b)
            st.session_state[salida_clave] = (resultado, registro)
            st.session_state[entrada_clave] = resultado.hex(' ') if utf8 else resultado
            st.session_state.pop(vuelta_clave, None)
            if utf8:
                st.session_state['formato_256'] = 'Hexadecimal'
        except ValueError as error:
            st.error(str(error))
    if salida_clave in st.session_state:
        resultado, registro = st.session_state[salida_clave]
        st.subheader('Mensaje cifrado')
        st.code(resultado.hex(' ') if utf8 else resultado, language=None)
        if utf8 and st.checkbox('Ver bytes cifrados en decimal'):
            st.code(' '.join(map(str, resultado)), language=None)
        st.caption('Usa el botón de copiar del bloque para guardar la secuencia. Para recuperarla necesitas el mismo modo, a y b.')
        mostrar_procedimiento(registro, 'encriptación')
    formato = st.radio('Formato de la secuencia cifrada', ['Hexadecimal', 'Decimal'], key='formato_256') if utf8 else None
    entrada = st.text_area('Mensaje cifrado para desencriptar', key=entrada_clave, max_chars=40000)
    if st.button('Desencriptar mensaje', type='primary', disabled=clave is None):
        st.session_state.pop(vuelta_clave, None)
        try:
            valores = leer_bytes(entrada, formato) if utf8 else entrada
            st.session_state[vuelta_clave] = descifrar(valores, a, b)
        except ValueError as error:
            st.error(str(error))
    if vuelta_clave in st.session_state:
        resultado, registro = st.session_state[vuelta_clave]
        st.subheader('Mensaje recuperado')
        st.code(resultado, language=None)
        anterior = st.session_state.get(salida_clave)
        entrada_real = bytes(registro['entrada']) if utf8 else registro['entrada']
        if anterior and entrada_real == anterior[0] and registro['clave'] == anterior[1]['clave']:
            original = anterior[1]['texto'] if utf8 else anterior[1]['entrada']
            if resultado == original:
                st.success('Verificación: el texto recuperado es exactamente igual al original.')
        else:
            st.info('Sin original correspondiente no se puede verificar la igualdad. Una clave incorrecta también puede producir texto válido; no hay autenticación.')
        mostrar_procedimiento(registro, 'desencriptación')
else:
    st.title('Casos de uso')
    st.write('En esta sección se presentan cinco situaciones que muestran cómo utilizar el programa para encriptar, desencriptar, consultar operaciones matemáticas y validar los datos ingresados.')
    for caso in casos_uso:
        with st.expander(f"{caso['codigo']}. {caso['nombre']}"):
            st.markdown('**Objetivo**')
            st.write(caso['objetivo'])
            st.markdown('**Datos de entrada**')
            st.markdown('\n'.join('- ' + dato for dato in caso['entrada']))
            st.markdown('**Pasos del usuario**')
            st.markdown('\n'.join(f'{numero}. {paso}' for numero, paso in enumerate(caso['pasos'], 1)))
            st.markdown('**Respuesta del programa**')
            st.write(caso['respuesta'])
            for formula in caso['formulas']:
                st.latex(formula)
            st.markdown('**Resultado esperado**')
            st.code(caso['resultado'], language=None)
            st.write(caso['explicacion'])


if inversos_solicitados:
    st.divider()
    st.subheader('MCD e inverso modular: procedimientos compartidos')
    st.write('Cada par de valores a y m se desarrolla una sola vez. El desplazamiento b no cambia el MCD ni el inverso.')
    for a, m in sorted(inversos_solicitados):
        with st.expander(f'MCD e inverso: a = {a}, m = {m}'):
            mostrar_inverso(a, m)
