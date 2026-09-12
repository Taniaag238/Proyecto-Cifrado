import unicodedata


# [1]
def normalizar_charset(charset):
    charset = unicodedata.normalize("NFC", charset)

    resultado = ""

    for caracter in charset:
        if caracter not in resultado:
            resultado += caracter

    return resultado


# [2]
def preparar_texto(texto):
    return unicodedata.normalize("NFC", texto)


# [3]
def separar_charset(charset):
    mayusculas = ""
    minusculas = ""
    numeros = ""
    simbolos = ""

    for caracter in charset:

        if caracter.isupper():
            mayusculas += caracter

        elif caracter.islower():
            minusculas += caracter

        elif caracter.isdigit():
            numeros += caracter

        else:
            simbolos += caracter

    return mayusculas, minusculas, numeros, simbolos


# [4]
def buscar_grupo(caracter, grupos):

    for grupo in grupos:

        if caracter in grupo:
            return grupo

    return None


# [5]
def cifrar_cesar(texto, charset, modulo):

    texto = preparar_texto(texto)
    charset = normalizar_charset(charset)

    if len(charset) < 2:
        raise ValueError(
            "El conjunto de caracteres debe contener al menos dos caracteres."
        )

    if not isinstance(modulo, int):
        raise ValueError(
            "El módulo debe ser un número entero."
        )

    grupos = separar_charset(charset)

    resultado = ""

    for caracter in texto:

        grupo = buscar_grupo(
            caracter,
            grupos
        )

        if grupo is None or len(grupo) == 0:
            resultado += caracter
            continue

        posicion = grupo.index(caracter)

        nueva_posicion = (
            posicion + modulo
        ) % len(grupo)

        resultado += grupo[nueva_posicion]

    return resultado


# [6]
def descifrar_cesar(texto, charset, modulo):

    texto = preparar_texto(texto)
    charset = normalizar_charset(charset)

    if len(charset) < 2:
        raise ValueError(
            "El conjunto de caracteres debe contener al menos dos caracteres."
        )

    if not isinstance(modulo, int):
        raise ValueError(
            "El módulo debe ser un número entero."
        )

    grupos = separar_charset(charset)

    resultado = ""

    for caracter in texto:

        grupo = buscar_grupo(
            caracter,
            grupos
        )

        if grupo is None or len(grupo) == 0:
            resultado += caracter
            continue

        posicion = grupo.index(caracter)

        nueva_posicion = (
            posicion - modulo
        ) % len(grupo)

        resultado += grupo[nueva_posicion]

    return resultado


# [7]
def cifrar_atbash(texto, charset):

    texto = preparar_texto(texto)
    charset = normalizar_charset(charset)

    if len(charset) < 2:
        raise ValueError(
            "El conjunto de caracteres debe contener al menos dos caracteres."
        )

    grupos = separar_charset(charset)

    resultado = ""

    for caracter in texto:

        grupo = buscar_grupo(
            caracter,
            grupos
        )

        if grupo is None or len(grupo) == 0:
            resultado += caracter
            continue

        posicion = grupo.index(caracter)

        nueva_posicion = (
            len(grupo) - 1 - posicion
        )

        resultado += grupo[nueva_posicion]

    return resultado


# [8]
def descifrar_atbash(texto, charset):

    return cifrar_atbash(
        texto,
        charset
    )
