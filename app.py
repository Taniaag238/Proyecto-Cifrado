from flask import Flask, jsonify, render_template, request

from cifrados import (
    cifrar_atbash,
    cifrar_cesar
)

from analizador import detectar_cifrado


app = Flask(__name__)  # [27]

LONGITUD_MINIMA = 15  # [28]


def validar_charset(charset):  # [29]

    if not charset:
        raise ValueError("Debes proporcionar un conjunto de caracteres.")

    if len(set(charset)) < 2:
        raise ValueError(
            "El conjunto de caracteres debe contener al menos dos caracteres diferentes."
        )


def validar_mensaje(texto):  # [30]

    if not texto or not texto.strip():
        raise ValueError("El mensaje no puede estar vacío.")

    if len(texto.strip()) < LONGITUD_MINIMA:
        raise ValueError(
            "El mensaje debe contener al menos 15 caracteres."
        )


@app.route("/")  # [31]
def inicio():
    return render_template("index.html")


@app.route("/api/cifrar", methods=["POST"])  # [32]
def cifrar():

    try:

        datos = request.get_json()  # [33]

        texto = datos.get("texto", "")
        charset = datos.get("charset", "")
        tipo = datos.get("tipo", "")
        modulo = datos.get("modulo", 0)

        validar_mensaje(texto)
        validar_charset(charset)

        if tipo == "CESAR":  # [34]

            modulo = int(modulo)

            if modulo < 0:
                raise ValueError(
                    "El módulo no puede ser negativo."
                )

            resultado = cifrar_cesar(
                texto,
                charset,
                modulo
            )

        elif tipo == "ATBASH":  # [35]

            resultado = cifrar_atbash(
                texto,
                charset
            )

        else:
            raise ValueError(
                "Selecciona un método de cifrado."
            )

        return jsonify({
            "ok": True,
            "resultado": resultado
        })  # [36]

    except (ValueError, TypeError) as error:

        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400  # [37]


@app.route("/api/descifrar", methods=["POST"])  # [38]
def descifrar():

    try:

        datos = request.get_json()

        texto = datos.get("texto", "")
        charset = datos.get("charset", "")

        validar_mensaje(texto)
        validar_charset(charset)

        resultado = detectar_cifrado(
            texto,
            charset
        )  # [39]

        return jsonify({
            "ok": True,
            "tipo": resultado["tipo"],
            "modulo": resultado["modulo"],
            "resultado": resultado["texto"],
            "confianza": resultado["confianza"]
        })  # [40]

    except (ValueError, TypeError) as error:

        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400


if __name__ == "__main__":  # [41]

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )