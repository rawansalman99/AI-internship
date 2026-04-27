import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Helper: check if finger is up
def finger_up(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y

# Gesture classifier
def classify_gesture(landmarks):
    fingers = []

    # Thumb (horizontal comparison)
    fingers.append(landmarks[4].x < landmarks[3].x)

    # Other fingers
    fingers.append(finger_up(landmarks, 8, 6))   # Index
    fingers.append(finger_up(landmarks, 12, 10)) # Middle
    fingers.append(finger_up(landmarks, 16, 14)) # Ring
    fingers.append(finger_up(landmarks, 20, 18)) # Pinky

    # Convert to pattern
    pattern = tuple(fingers)

    if pattern == (True, False, False, False, False):
        return "Thumbs Up 👍"
    elif pattern == (False, False, False, False, False):
        return "Fist ✊"
    elif pattern == (True, True, True, True, True):
        return "Open Palm ✋"
    else:
        return "Unknown"

# Action mapping
def perform_action(gesture):
    if gesture == "Thumbs Up 👍":
        pyautogui.press("playpause")  # media key
    elif gesture == "Fist ✊":
        pyautogui.press("volumedown")
    elif gesture == "Open Palm ✋":
        pyautogui.press("volumeup")

# Start webcam
cap = cv2.VideoCapture(0)

prev_gesture = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for natural interaction
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            # Classify
            gesture = classify_gesture(lm)

            # Avoid repeating actions too fast
            if gesture != prev_gesture:
                perform_action(gesture)
                prev_gesture = gesture

            # Display gesture
            cv2.putText(frame, gesture, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()