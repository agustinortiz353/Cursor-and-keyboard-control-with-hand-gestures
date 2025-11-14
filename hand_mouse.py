import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np
import time

import utils  # <<--- LA SOLUCIÓN

pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

class HandMouse:
    def __init__(self, smooth=0.45, click_thresh=0.045, delta=5):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
        )
        self.drawing = mp.solutions.drawing_utils
        self.smooth = smooth
        self.click_thresh = click_thresh
        self.delta = delta
        self.prev_x = 0
        self.prev_y = 0
        self.right_pressed = False
        self.last_voice_toggle = 0
        self.last_enter_time = 0

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        result = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            self.drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            # Movimiento de mano -> cursor
            palm = np.mean([[hand.landmark[i].x, hand.landmark[i].y] 
                            for i in [0, 1, 5, 9, 13, 17]], axis=0)

            mapped_x = np.clip((palm[0] - 0.35) * 2.5, 0, 1)
            mapped_y = np.clip((palm[1] - 0.35) * 2.5, 0, 1)
            target_x, target_y = int(mapped_x * screen_w), int(mapped_y * screen_h)

            if abs(target_x - self.prev_x) > self.delta or abs(target_y - self.prev_y) > self.delta:
                self.prev_x = int(self.prev_x * (1 - self.smooth) + target_x * self.smooth)
                self.prev_y = int(self.prev_y * (1 - self.smooth) + target_y * self.smooth)
                pyautogui.moveTo(self.prev_x, self.prev_y)

            # Distancias
            d = lambda a, b: math.hypot(a.x - b.x, a.y - b.y)
            thumb, index, middle, ring, pinky = [hand.landmark[i] for i in [4, 8, 12, 16, 20]]
            d_thumb_index = d(thumb, index)
            d_thumb_middle = d(thumb, middle)
            d_thumb_ring = d(thumb, ring)
            d_thumb_pinky = d(thumb, pinky)

            # Click izquierdo
            if d_thumb_index < self.click_thresh:
                pyautogui.mouseDown(button='left')
            else:
                pyautogui.mouseUp(button='left')

            # Click derecho
            if d_thumb_middle < self.click_thresh and not self.right_pressed:
                pyautogui.click(button='right')
                self.right_pressed = True
            elif d_thumb_middle >= self.click_thresh:
                self.right_pressed = False

            # Enter
            if d_thumb_ring < self.click_thresh and time.time() - self.last_enter_time > 1:
                pyautogui.press('enter')
                self.last_enter_time = time.time()

            # Toggle dictado (meñique)
            if d_thumb_pinky < 0.05 and time.time() - self.last_voice_toggle > 1:
                utils.listening = not utils.listening
                self.last_voice_toggle = time.time()

        else:
            pyautogui.mouseUp(button='left')

        cv2.putText(
            frame,
            f"Voz: {'ON' if utils.listening else 'OFF'}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        return frame
