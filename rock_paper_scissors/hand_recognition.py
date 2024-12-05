import cv2
import mediapipe as mp

class HandRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hand(self, frame):
        """识别手势并返回结果，支持剪刀、石头、布"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if not results.multi_hand_landmarks:
            return None

        gestures = []
        for hand_landmarks in results.multi_hand_landmarks:
            fingers = self._count_fingers(hand_landmarks)
            if fingers == [0, 0, 0, 0, 0]:
                gestures.append("rock")  # 石头
            elif fingers == [1, 1, 1, 1, 1]:
                gestures.append("paper")  # 布
            elif fingers == [0, 1, 1, 0, 0]:
                gestures.append("scissors")  # 剪刀
            else:
                gestures.append("unknown")  # 未知手势
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return gestures

    def _count_fingers(self, hand_landmarks):
        """根据手部关键点判断手势"""
        tips_ids = [4, 8, 12, 16, 20]
        fingers = []
        for idx, tip_id in enumerate(tips_ids):
            if idx == 0:  # 大拇指特殊处理
                fingers.append(hand_landmarks.landmark[tip_id].x < hand_landmarks.landmark[tip_id - 1].x)
            else:
                fingers.append(hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y)
        return fingers