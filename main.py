from hand_mouse import HandMouse
from talk import start_dictado_thread
import cv2, pyautogui

pyautogui.FAILSAFE = False

if __name__ == "__main__":
    
    start_dictado_thread()  # single dictation thread 
    cap = cv2.VideoCapture(0)
    controller = HandMouse()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("🖐️ Control Mano", controller.process_frame(frame))
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release() 
        cv2.destroyAllWindows()


