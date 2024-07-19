import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose

# 肩の傾きを評価する関数(直立に立っているかの指標)
def calculate_shoulder_score(pose_landmarks):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # 右肩と左肩の傾きを計算
    angle = calculate_shoulder_angle(left_shoulder, right_shoulder)
    
    if 0 <= angle <= 5:
        score = 3  # 満点
    elif 5 < angle <= 10:
        score = 2  # 中間
    elif 10 < angle <= 15:
        score = 1  # 低い
    else:
        score = 0  # 不適切
    
    return score, angle

# 右肩と左肩の傾きを計算
def calculate_shoulder_angle(left_shoulder, right_shoulder):
    delta_x = left_shoulder.x - right_shoulder.x
    delta_y = left_shoulder.y - right_shoulder.y
    
    angle = np.degrees(np.arctan2(delta_y, delta_x))
    upright_angle = np.abs(angle)
    
    return upright_angle