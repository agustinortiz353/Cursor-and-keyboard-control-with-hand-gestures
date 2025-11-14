# Cursor and Keyboard Control with Hand Gestures

This project allows you to control your mouse cursor and keyboard input using hand gestures captured via a webcam. By leveraging **MediaPipe** for hand tracking and **PyAutoGUI** for mouse and keyboard automation, you can interact with your computer without touching any physical devices.

## Features

- **Cursor Control:** Move the mouse cursor by moving the palm of your hand.  
- **Left Click:** Perform a left click by touching your thumb and index finger together.  
- **Right Click:** Perform a right click by touching your thumb and middle finger together.  
- **Drawing Mode:** Activate a "drawing mode" using voice commands to hold down the left click while moving the hand, enabling freehand drawing on the screen.  
- **Voice Dictation:** Use voice commands to type text directly into any application.  
- **Visual Feedback:** Real-time on-screen indicators show the current mode and dictation status.

## Requirements

- Python 3.8+  
- OpenCV  
- MediaPipe  
- PyAutoGUI  
- SpeechRecognition  
- NumPy

## How It Works

1. The webcam captures your hand movements.  
2. MediaPipe detects hand landmarks and tracks finger positions.  
3. Gestures (thumb + index, thumb + middle) trigger mouse actions.  
4. Voice commands can activate drawing mode or type text in real-time.  
5. The cursor moves smoothly following your palm position.

## Use Cases

- Hands-free computer interaction  
- Digital drawing or annotation  
- Accessibility tool for users with limited mobility  

