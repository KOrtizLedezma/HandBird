import threading
import cv2
import mediapipe as mp
import time

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.cam = cv2.VideoCapture(0)
        self.gesture_fist_detected = False
        self.running = True
        self.thread = threading.Thread(target=self._detect_loop)
        self.thread.daemon = True
        self.thread.start()
        self.mp_draw = mp.solutions.drawing_utils

    def _is_fist(self, landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_bases = [3, 5, 9, 13, 17]

        folded_fingers = 0
        for tip, base in zip(finger_tips, finger_bases):
            if landmarks[tip].y > landmarks[base].y:
                folded_fingers += 1

        return folded_fingers >= 4

    def _detect_loop(self):
        while self.running:
            success, frame = self.cam.read()
            if not success:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            self.gesture_fist_detected = False

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:

                    self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)

                    if self._is_fist(handLms.landmark):
                        self.gesture_fist_detected = True
                        cv2.putText(frame, "Jumping", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        break

            # frame = cv2.flip(frame, 1)
            cv2.putText(frame, "Make a fist to jump!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

            time.sleep(0.05)

    def stop(self):
        self.running = False
        self.thread.join()
        self.cam.release()
        cv2.destroyAllWindows()
