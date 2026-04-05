import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
import random

app = Flask(__name__)
CORS(app) 
# ===== INTENTS =====
intents = {
    "wifi_no_conecta": {
        "training": [
            "no se conecta al wifi",
            "mi tv no conecta a internet",
            "no tengo conexion",
            "no conecta al internet",
            "problema de wifi"
        ],
        "responses": [
            "Verifica que el WiFi esté activado en tu Smart TV. Luego reinicia el televisor y el router.",
            "Intenta acercar el televisor al router y vuelve a conectarte a la red.",
            "Asegúrate de que otros dispositivos sí puedan conectarse al WiFi."
        ]
    },

    "red_no_aparece": {
        "training": [
            "no aparece la red",
            "no veo mi wifi",
            "mi red no sale",
            "no detecta wifi",
            "no encuentra red"
        ],
        "responses": [
            "Reinicia el router y espera 2 minutos antes de buscar la red nuevamente.",
            "Verifica que el WiFi esté activado en tu Smart TV.",
            "Acércate al router e intenta escanear redes otra vez."
        ]
    },

    "contrasena_incorrecta": {
        "training": [
            "contraseña incorrecta",
            "clave incorrecta",
            "no acepta la contraseña",
            "password error",
            "clave wifi no funciona"
        ],
        "responses": [
            "Verifica que estés escribiendo correctamente la contraseña (respeta mayúsculas y minúsculas).",
            "Intenta olvidar la red y volver a conectarte.",
            "Reinicia el router y vuelve a intentar."
        ]
    },

    "internet_lento": {
        "training": [
            "internet lento",
            "wifi lento",
            "se traba netflix",
            "video lento",
            "conexion lenta"
        ],
        "responses": [
            "Intenta reiniciar tu router para mejorar la velocidad.",
            "Cierra aplicaciones en segundo plano en el Smart TV.",
            "Acércate al router o usa cable Ethernet para mejor conexión."
        ]
    },

    "error_conexion": {
        "training": [
            "error de conexion",
            "no hay internet",
            "sin conexion",
            "error red",
            "fallo de conexion"
        ],
        "responses": [
            "Reinicia tu router y el televisor.",
            "Verifica si otros dispositivos tienen internet.",
            "Comprueba la configuración de red en el Smart TV."
        ]
    },

    "ethernet": {
        "training": [
            "cable ethernet",
            "conexion por cable",
            "no funciona cable",
            "ethernet no conecta",
            "lan error"
        ],
        "responses": [
            "Asegúrate de que el cable esté bien conectado.",
            "Prueba con otro cable Ethernet.",
            "Reinicia el router y verifica la configuración de red."
        ]
    },

    "reiniciar_router": {
        "training": [
            "reiniciar router",
            "como reiniciar wifi",
            "resetear modem",
            "reiniciar internet",
            "apagar router"
        ],
        "responses": [
            "Desconecta el router por 30 segundos y vuelve a encenderlo.",
            "Espera a que todas las luces se estabilicen antes de usarlo.",
            "Luego intenta conectar el Smart TV nuevamente."
        ]
    },

    "configuracion_inicial": {
        "training": [
            "configurar smart tv",
            "configuracion inicial",
            "como conectar tv a internet",
            "primer uso",
            "setup tv"
        ],
        "responses": [
            "Ve a Configuración > Red > Conectar a WiFi y selecciona tu red.",
            "Introduce la contraseña del WiFi correctamente.",
            "Sigue los pasos en pantalla para completar la configuración."
        ]
    },

    "saludo": {
        "training": [
            "hola",
            "buenas",
            "hello",
            "hi",
            "que tal"
        ],
        "responses": [
            "Hola, soy tu asistente de Smart TV. ¿En qué problema te puedo ayudar?"
        ]
    },

    "despedida": {
        "training": [
            "gracias",
            "adios",
            "bye",
            "nos vemos",
            "ok gracias",
            "ya funciona"
        ],
        "responses": [
            "¡Con gusto! Si tienes otro problema, aquí estaré 😊",
            "¡Éxitos con tu Smart TV!",
            "Hasta luego 👋"
        ]
    }
}

# ===== FUNCION CHATBOT =====
def detectar_intent(mensaje):
    mensaje = mensaje.lower()

    for intent, data in intents.items():
        for frase in data["training"]:
            palabras = frase.split()

            coincidencias = 0
            for palabra in palabras:
                if palabra in mensaje:
                    coincidencias += 1

            # 🔥 si coincide al menos 50%
            if coincidencias >= len(palabras) / 2:
                return intent

    return "fallback"


def responder(mensaje):
    intent = detectar_intent(mensaje)

    if intent == "fallback":
        return "No entendí tu problema, ¿puedes explicarlo de otra forma?"

    return random.choice(intents[intent]["responses"])


# ===== API =====
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensaje = data.get("mensaje", "")

    respuesta = responder(mensaje)

    return jsonify({"respuesta": respuesta})


@app.route("/", methods=["GET"])
def home():
    return "Servidor funcionando 👍"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)        