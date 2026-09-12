
const charset = document.getElementById("charset"); // [80]
const tecladoCharset = document.getElementById("tecladoCharset"); // [81]
const nuevoCaracter = document.getElementById("nuevoCaracter"); // [82]

const texto = document.getElementById("texto"); // [83]
const tipoCifrado = document.getElementById("tipoCifrado"); // [84]
const modulo = document.getElementById("modulo"); // [85]
const campoModulo = document.getElementById("campoModulo"); // [86]

const btnCifrar = document.getElementById("btnCifrar"); // [87]
const btnDescifrar = document.getElementById("btnDescifrar"); // [88]
const btnAgregarCaracter = document.getElementById("btnAgregarCaracter"); // [89]
const btnBorrarCaracter = document.getElementById("btnBorrarCaracter"); // [90]
const btnLimpiarTexto = document.getElementById("btnLimpiarTexto"); // [91]

const resultadoCifrado =
    document.getElementById("resultadoCifrado"); // [92]

const textoResultadoCifrado =
    document.getElementById("textoResultadoCifrado"); // [93]

const panelDescifrar =
    document.getElementById("panelDescifrar"); // [94]

const textoDescifrar =
    document.getElementById("textoDescifrar"); // [95]

const seccionResultadoDescifrado =
    document.getElementById("seccionResultadoDescifrado"); // [96]

const textoResultadoDescifrado =
    document.getElementById("textoResultadoDescifrado"); // [97]

const metodoDetectado =
    document.getElementById("metodoDetectado"); // [98]

const moduloDetectado =
    document.getElementById("moduloDetectado"); // [99]

const confianzaDetectada =
    document.getElementById("confianzaDetectada"); // [100]

const charsetInicial =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + // [101]
    "abcdefghijklmnopqrstuvwxyz" + // [102]
    "ÑñÁÉÍÓÚáéíóúÜü" + // [103]
    "0123456789" + // [104]
    " .,;:!?¿¡-_()[]{}@#%&=+/" + // [105]
    "😀😃😄😁😂🙂🙃😉😊😎😍👍👎⭐🔥🎉🚀"; // [106]

charset.value = charsetInicial; // [107]

function mostrarTeclado() { // [108]
    tecladoCharset.innerHTML = ""; // [109]

    for (const caracter of charset.value) { // [110]
        const boton = document.createElement("button"); // [111]

        boton.type = "button"; // [112]
        boton.className = "tecla"; // [113]

        if (caracter === " ") { // [114]
            boton.textContent = "ESPACIO"; // [115]
            boton.classList.add("espacio"); // [116]
            boton.title = "Agregar espacio"; // [117]
        } else {
            boton.textContent = caracter; // [118]
            boton.title = `Agregar "${caracter}"`; // [119]
        }

        boton.addEventListener("click", () => { // [120]
            texto.value += caracter; // [121]
            texto.focus(); // [122]
        });

        tecladoCharset.appendChild(boton); // [123]
    }
}

function actualizarMetodo() { // [124]
    if (tipoCifrado.value === "CESAR") { // [125]
        campoModulo.classList.remove("oculto"); // [126]

        requestAnimationFrame(() => { // [127]
            campoModulo.classList.remove("ocultando"); // [128]
        });

        return; // [129]
    }

    campoModulo.classList.add("ocultando"); // [130]

    setTimeout(() => { // [131]
        if (tipoCifrado.value === "ATBASH") { // [132]
            campoModulo.classList.add("oculto"); // [133]
        }
    }, 180);
}

function mostrarError(mensaje) { // [134]
    Swal.fire({ // [135]
        icon: "error", // [136]
        title: "No se puede continuar", // [137]
        text: mensaje, // [138]
        confirmButtonText: "Aceptar", // [139]
        confirmButtonColor: "#244568" // [140]
    });
}

function mostrarAviso(mensaje) { // [141]
    Swal.fire({ // [142]
        icon: "warning", // [143]
        title: "Revisa el mensaje", // [144]
        text: mensaje, // [145]
        confirmButtonText: "Aceptar", // [146]
        confirmButtonColor: "#244568" // [147]
    });
}

function obtenerModulo() { // [148]
    const valor = Number(modulo.value); // [149]

    if (!Number.isInteger(valor) || valor < 0) { // [150]
        return null; // [151]
    }

    return valor; // [152]
}

function validarCharset() { // [153]
    if (!charset.value) { // [154]
        mostrarAviso( // [155]
            "El conjunto de caracteres no puede estar vacío."
        );

        return false; // [156]
    }

    if ([...charset.value].length < 2) { // [157]
        mostrarAviso( // [158]
            "El conjunto debe contener al menos dos caracteres."
        );

        return false; // [159]
    }

    return true; // [160]
}

function validarMensaje(mensaje) { // [161]
    if (mensaje.trim().length < 15) { // [162]
        mostrarAviso( // [163]
            "El mensaje debe contener al menos 15 caracteres."
        );

        return false; // [164]
    }

    return true; // [165]
}

tipoCifrado.addEventListener( // [166]
    "change",
    actualizarMetodo
);

btnAgregarCaracter.addEventListener( // [167]
    "click",
    () => {
        const caracter = nuevoCaracter.value; // [168]

        if (!caracter) { // [169]
            mostrarAviso(
                "Escribe un carácter antes de agregarlo."
            );

            return; // [170]
        }

        if ([...caracter].length !== 1) { // [171]
            mostrarAviso(
                "Solo puedes agregar un carácter a la vez."
            );

            return; // [172]
        }

        if (charset.value.includes(caracter)) { // [173]
            mostrarAviso(
                "Ese carácter ya forma parte del conjunto."
            );

            return; // [174]
        }

        charset.value += caracter; // [175]
        nuevoCaracter.value = ""; // [176]

        mostrarTeclado(); // [177]

        Swal.fire({ // [178]
            icon: "success",
            title: "Carácter agregado",
            text: "El carácter se agregó al conjunto correctamente.",
            confirmButtonText: "Aceptar",
            confirmButtonColor: "#244568"
        });
    }
);

nuevoCaracter.addEventListener( // [179]
    "keydown",
    (evento) => {
        if (evento.key === "Enter") { // [180]
            evento.preventDefault(); // [181]
            btnAgregarCaracter.click(); // [182]
        }
    }
);

btnBorrarCaracter.addEventListener( // [183]
    "click",
    () => {
        const caracteres = [...charset.value]; // [184]

        if (caracteres.length === 0) { // [185]
            return;
        }

        caracteres.pop(); // [186]

        charset.value =
            caracteres.join(""); // [187]

        mostrarTeclado(); // [188]
    }
);

btnLimpiarTexto.addEventListener( // [189]
    "click",
    () => {
        texto.value = ""; // [190]
        texto.focus(); // [191]
    }
);

btnCifrar.addEventListener( // [192]
    "click",
    async () => {
        if (!validarMensaje(texto.value)) { // [193]
            return;
        }

        if (!validarCharset()) { // [194]
            return;
        }

        let moduloValor = 0; // [195]

        if (tipoCifrado.value === "CESAR") { // [196]
            moduloValor = obtenerModulo(); // [197]

            if (moduloValor === null) { // [198]
                mostrarAviso(
                    "El módulo debe ser un número entero mayor o igual a cero."
                );

                return; // [199]
            }
        }

        const datos = { // [200]
            texto: texto.value,
            charset: charset.value,
            tipo: tipoCifrado.value,
            modulo: moduloValor
        };

        try {
            const respuesta = await fetch( // [201]
                "/api/cifrar",
                {
                    method: "POST", // [202]

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(datos) // [203]
                }
            );

            const resultado =
                await respuesta.json(); // [204]

            if (!respuesta.ok || !resultado.ok) { // [205]
                mostrarError(
                    resultado.error ||
                    "No fue posible cifrar el mensaje."
                );

                return; // [206]
            }

            textoResultadoCifrado.textContent =
                resultado.resultado; // [207]

            resultadoCifrado.hidden = false; // [208]

            textoDescifrar.value =
                resultado.resultado; // [209]

            panelDescifrar.hidden = false; // [210]

            seccionResultadoDescifrado.hidden = true; // [211]

            panelDescifrar.scrollIntoView({ // [212]
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {
            mostrarError( // [213]
                "No fue posible comunicarse con el servidor."
            );
        }
    }
);

btnDescifrar.addEventListener( // [214]
    "click",
    async () => {
        if (!validarMensaje(textoDescifrar.value)) { // [215]
            return;
        }

        if (!validarCharset()) { // [216]
            return;
        }

        const datos = { // [217]
            texto: textoDescifrar.value,
            charset: charset.value
        };

        try {
            const respuesta = await fetch( // [218]
                "/api/descifrar",
                {
                    method: "POST", // [219]

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(datos) // [220]
                }
            );

            const resultado =
                await respuesta.json(); // [221]

            if (!respuesta.ok || !resultado.ok) { // [222]
                mostrarError(
                    resultado.error ||
                    "No fue posible descifrar el mensaje."
                );

                return; // [223]
            }

            textoResultadoDescifrado.textContent =
                resultado.resultado; // [224]

            metodoDetectado.textContent =
                resultado.tipo; // [225]

            moduloDetectado.textContent =
                resultado.tipo === "CESAR"
                    ? resultado.modulo
                    : "No aplica"; // [226]

            const confianza =
                Number(resultado.confianza); // [227]

            confianzaDetectada.textContent =
                Number.isFinite(confianza)
                    ? `${(confianza * 100).toFixed(1)}%`
                    : "No disponible"; // [228]

            seccionResultadoDescifrado.hidden =
                false; // [229]

            seccionResultadoDescifrado.scrollIntoView({ // [230]
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {
            mostrarError( // [231]
                "No fue posible comunicarse con el servidor."
            );
        }
    }
);

actualizarMetodo(); // [232]
mostrarTeclado(); // [233]

