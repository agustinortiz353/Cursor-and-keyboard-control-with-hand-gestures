# utils.py
import threading
import speech_recognition as sr

# ------------------ VARIABLES GLOBALES ------------------
listening = False
dictado_thread = None
borrar_flag = False
last_text = ""
buffer_text = ""
lock = threading.Lock()  # para sincronizar escritura

# ------------------ CONSTANTES ------------------
EXCLAMATIVAS = ["pelotudo", "imbecil"]

# ------------------ RECOGNICION ------------------
recognizer = sr.Recognizer()
mic = sr.Microphone()

def reemplazar_signos(texto: str) -> str:
    return texto.replace("signo de pregunta", "?").replace("signo de exclamación", "!")
