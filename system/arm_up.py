import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose

# 腕が真上に上がっているかを評価する関数(肩と手首の距離を測定)
def calculate_arm_up_score(pose_landmarks, image_width):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

    # 肩と手首のx軸の距離を計算
    left_arm_up_distance = calculate_arm_up_distance(left_shoulder, left_wrist, image_width)
    right_arm_up_distance = calculate_arm_up_distance(right_shoulder, right_wrist, image_width)
    
    score = calculate_arm_up_score_values(left_arm_up_distance, right_arm_up_distance)
    
    return score, left_arm_up_distance, right_arm_up_distance

# 肩と手首のx軸の距離を計算
def calculate_arm_up_distance(shoulder, wrist, image_width):
    delta_x = (wrist.x - shoulder.x) * image_width
    distance = np.abs(delta_x)
    return distance

# 腕が真上に上がっているかのスコア
def calculate_arm_up_score_values(left_arm_up_distance, right_arm_up_distance):
    if left_arm_up_distance <= 100 and right_arm_up_distance <= 100:
        score = 3  # 満点
    elif left_arm_up_distance <= 150 and right_arm_up_distance <= 150:
        score = 2  # 中間
    elif left_arm_up_distance <= 200 and right_arm_up_distance <= 200:
        score = 1  # 低い
    else:
        score = 0  # 不適切
    return score