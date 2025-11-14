# talk.py
import threading
import time
import pyperclip
import pyautogui
import utils

def listen_and_type_continuous():
    # nota: no hacemos "from utils import ..." para evitar copias
    with utils.mic as source:
        utils.recognizer.adjust_for_ambient_noise(source)
        while True:
            if not utils.listening:
                time.sleep(0.1)
                continue
            try:
                audio = utils.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                texto_google = utils.recognizer.recognize_google(audio, language="es-AR")
                texto_corregido = " " + texto_google
                texto_corregido = utils.reemplazar_signos(texto_corregido)

                with utils.lock:
                    utils.buffer_text += texto_corregido

                    if "borrar" in utils.buffer_text:
                        utils.borrar_flag = True
                        threading.Thread(target=modo_borrar, daemon=True).start()
                        utils.buffer_text = ""
                    else:
                        if utils.buffer_text != utils.last_text:
                            texto_a_escribir = utils.buffer_text[len(utils.last_text):]
                            pyperclip.copy(texto_a_escribir)
                            pyautogui.hotkey('ctrl', 'v')
                            utils.last_text = utils.buffer_text

            except (utils.recognizer.WaitTimeoutError if hasattr(utils.recognizer, 'WaitTimeoutError') else Exception, 
                    Exception):
                # no spameamos errores; en producción podés loguear
                continue

def modo_borrar():
    start = time.time()
    while time.time() - start < 3 and utils.last_text:
        pyautogui.press('backspace')
        with utils.lock:
            utils.last_text = utils.last_text[:-1]
            utils.buffer_text = utils.buffer_text[:-1]
        time.sleep(0.01)
    utils.borrar_flag = False

def start_dictado_thread():
    if utils.dictado_thread is None or not utils.dictado_thread.is_alive():
        utils.dictado_thread = threading.Thread(target=listen_and_type_continuous, daemon=True)
        utils.dictado_thread.start()
