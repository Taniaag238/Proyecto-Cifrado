import re
import unicodedata

from cifrados import (
    descifrar_cesar,
    descifrar_atbash,
    separar_charset
)


# [09]
FRECUENCIAS_ES = {
    "E": 0.1369,
    "A": 0.1253,
    "O": 0.0868,
    "L": 0.0826,
    "S": 0.0798,
    "N": 0.0700,
    "R": 0.0687,
    "D": 0.0586,
    "I": 0.0625,
    "T": 0.0463,
    "C": 0.0402,
    "U": 0.0393,
    "M": 0.0241,
    "P": 0.0251,
    "B": 0.0142,
    "G": 0.0101,
    "V": 0.0090,
    "Y": 0.0101,
    "Q": 0.0088,
    "H": 0.0070,
    "F": 0.0069,
    "Z": 0.0052,
    "J": 0.0044,
    "Ñ": 0.0031,
    "X": 0.0022,
    "K": 0.0011,
    "W": 0.0002
}


# [10]
PALABRAS_ES = {
    "EL", "LA", "LOS", "LAS", "UN", "UNA", "UNO",
    "DE", "DEL", "AL", "EN", "QUE", "Y", "A",
    "PARA", "POR", "CON", "SIN", "NO", "SI",
    "SE", "SU", "SUS", "LO", "LE", "LES",
    "COMO", "PERO", "ME", "TE", "ES", "SON",
    "ESTA", "ESTE", "ESTOS", "ESTAS",
    "FUE", "SER", "TIENE", "TIENEN", "HAY",
    "MUY", "MAS", "YA", "CUANDO", "DONDE",
    "QUIEN", "QUIENES", "TODO", "TODOS",
    "TAMBIEN", "TODA", "TODAS", "OTRO",
    "OTRA", "OTROS", "OTRAS", "MI", "MIS",
    "TU", "TUS", "SU", "SE", "NO",
    "COMPLETO", "MENSAJE", "TEXTO",
    "DATOS", "SEGURIDAD", "INFORMACION",
    "PRUEBA", "PRUEBAS", "METODO", "METODOS",
    "CIFRADO", "CIFRADOS", "DESCIFRAR",
    "DESCIFRADO", "CESAR", "ATBASH",
    "SISTEMA", "SISTEMAS", "PROGRAMA",
    "PROBAR", "IMPORTANTE", "CORRECTO",
    "CORRECTA", "HOLA", "MUNDO"
}


# [11]
NGRAMAS_ES = {
    "DE", "EL", "LA", "EN", "ES", "ER",
    "AR", "RE", "OS", "AS", "SE", "AN",
    "AL", "UN", "ON", "TE", "RA", "ST",
    "QUE", "ENT", "LOS", "LAS", "DEL",
    "POR", "PAR", "CON", "EST", "ADO",
    "ARA", "ION", "UNA", "TRA", "NTE",
    "RES", "ANTE", "ENTRE", "CION",
    "CIÓN", "DAD", "MENTE", "PRO",
    "PRE", "COM", "DES", "CIF", "SEG",
    "INF", "MEN", "SAJ"
}


# [12]
def preparar_analisis(texto):
    texto = unicodedata.normalize("NFC", texto)
    return texto.upper()


# [13]
def normalizar_letras(texto):
    texto = preparar_analisis(texto)

    reemplazos = {
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
        "Ü": "U"
    }

    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)

    return texto


# [14]
def obtener_letras(texto):
    texto = normalizar_letras(texto)

    return re.findall(
        r"[A-ZÑ]",
        texto
    )


# [15]
def obtener_frecuencias(texto):
    letras = obtener_letras(texto)

    if not letras:
        return {}

    frecuencias = {}

    for letra in letras:
        frecuencias[letra] = (
            frecuencias.get(letra, 0) + 1
        )

    total = len(letras)

    for letra in frecuencias:
        frecuencias[letra] /= total

    return frecuencias


# [16]
def obtener_frecuencias_esperadas():
    total = sum(FRECUENCIAS_ES.values())

    if total == 0:
        return FRECUENCIAS_ES.copy()

    return {
        letra: frecuencia / total
        for letra, frecuencia in FRECUENCIAS_ES.items()
    }


# [17]
def puntuacion_chi_cuadrado(texto):
    letras = obtener_letras(texto)

    if not letras:
        return 0

    frecuencias_observadas = obtener_frecuencias(texto)
    frecuencias_esperadas = obtener_frecuencias_esperadas()

    total = len(letras)
    chi = 0

    for letra, esperada in frecuencias_esperadas.items():

        observada = frecuencias_observadas.get(
            letra,
            0
        )

        esperado = esperada * total

        if esperado <= 0:
            continue

        observado = observada * total

        chi += (
            (observado - esperado) ** 2
        ) / esperado

    return chi


# [18]
def puntuacion_frecuencia(texto):
    letras = obtener_letras(texto)

    if not letras:
        return 0

    chi = puntuacion_chi_cuadrado(texto)

    puntuacion = 100 / (1 + chi)

    return puntuacion


# [19]
def obtener_palabras(texto):
    return re.findall(
        r"[A-ZÑ]+",
        normalizar_letras(texto)
    )


# [20]
def puntuacion_palabras(texto):
    palabras = obtener_palabras(texto)

    if not palabras:
        return 0

    puntuacion = 0

    for palabra in palabras:

        if palabra in PALABRAS_ES:
            if len(palabra) <= 2:
                puntuacion += 4
            elif len(palabra) <= 4:
                puntuacion += 8
            else:
                puntuacion += 12

    maximo = len(palabras) * 12

    if maximo == 0:
        return 0

    return (
        puntuacion / maximo
    ) * 100


# [21]
def puntuacion_ngramas(texto):
    texto = normalizar_letras(texto)

    letras = obtener_letras(texto)

    if len(letras) < 2:
        return 0

    puntuacion = 0
    total = 0

    for ngrama in NGRAMAS_ES:

        cantidad = texto.count(ngrama)

        if cantidad > 0:
            longitud = len(ngrama)

            puntuacion += (
                cantidad * longitud
            )

    for i in range(len(letras) - 1):
        total += 1

    if total == 0:
        return 0

    valor = (
        puntuacion / max(total, 1)
    ) * 20

    return min(100, valor)


# [22]
def puntuacion_espanol(texto):
    letras = obtener_letras(texto)

    if not letras:
        return 0

    frecuencia = puntuacion_frecuencia(texto)
    palabras = puntuacion_palabras(texto)
    ngramas = puntuacion_ngramas(texto)

    if len(letras) < 5:
        return (
            frecuencia * 0.70
            + palabras * 0.20
            + ngramas * 0.10
        )

    if len(letras) < 15:
        return (
            frecuencia * 0.45
            + palabras * 0.40
            + ngramas * 0.15
        )

    return (
        frecuencia * 0.35
        + palabras * 0.45
        + ngramas * 0.20
    )


# [23]
def detectar_cesar(texto, charset):
    candidatos = []

    grupos = separar_charset(charset)

    tamanos = [
        len(grupo)
        for grupo in grupos
        if len(grupo) > 0
    ]

    cantidad_modulos = max(
        tamanos,
        default=0
    )

    if cantidad_modulos == 0:
        return candidatos

    for modulo in range(cantidad_modulos):

        candidato = descifrar_cesar(
            texto,
            charset,
            modulo
        )

        puntuacion = puntuacion_espanol(
            candidato
        )

        candidatos.append({
            "tipo": "CESAR",
            "modulo": modulo,
            "texto": candidato,
            "puntuacion": puntuacion
        })

    return candidatos


# [24]
def detectar_atbash(texto, charset):
    candidato = descifrar_atbash(
        texto,
        charset
    )

    puntuacion = puntuacion_espanol(
        candidato
    )

    return {
        "tipo": "ATBASH",
        "modulo": None,
        "texto": candidato,
        "puntuacion": puntuacion
    }


# [25]
def calcular_confianza(candidatos):
    if not candidatos:
        return 0

    if len(candidatos) == 1:
        return 0.5

    primero = candidatos[0]["puntuacion"]
    segundo = candidatos[1]["puntuacion"]

    if primero <= 0:
        return 0

    calidad = min(
        1,
        primero / 100
    )

    diferencia = max(
        0,
        primero - segundo
    )

    separacion = min(
        1,
        diferencia / 20
    )

    confianza = (
        calidad * 0.55
        + separacion * 0.45
    )

    confianza = max(
        0,
        min(0.99, confianza)
    )

    return round(
        confianza,
        4
    )


# [26]
def detectar_cifrado(texto, charset):
    texto = unicodedata.normalize(
        "NFC",
        texto
    )

    charset = unicodedata.normalize(
        "NFC",
        charset
    )

    if not texto:
        return {
            "tipo": "DESCONOCIDO",
            "modulo": None,
            "texto": texto,
            "confianza": 0
        }

    if not charset:
        return {
            "tipo": "DESCONOCIDO",
            "modulo": None,
            "texto": texto,
            "confianza": 0
        }

    candidatos = []

    candidatos.extend(
        detectar_cesar(
            texto,
            charset
        )
    )

    candidatos.append(
        detectar_atbash(
            texto,
            charset
        )
    )

    candidatos = [
        candidato
        for candidato in candidatos
        if candidato["texto"] is not None
    ]

    candidatos.sort(
        key=lambda candidato: candidato["puntuacion"],
        reverse=True
    )

    if not candidatos:
        return {
            "tipo": "DESCONOCIDO",
            "modulo": None,
            "texto": texto,
            "confianza": 0
        }

    mejor = candidatos[0]

    letras = obtener_letras(
        mejor["texto"]
    )

    if not letras:
        return {
            "tipo": "DESCONOCIDO",
            "modulo": None,
            "texto": texto,
            "confianza": 0
        }

    return {
        "tipo": mejor["tipo"],
        "modulo": mejor["modulo"],
        "texto": mejor["texto"],
        "confianza": calcular_confianza(
            candidatos
        )
    }