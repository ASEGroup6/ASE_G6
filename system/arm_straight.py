import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose




# 腕が直線かを評価する関数
def calculate_arm_position_score(pose_landmarks):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    right_elbow = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

    upper_arm_left = np.array([left_elbow.x - left_shoulder.x, left_elbow.y - left_shoulder.y])
    lower_arm_left = np.array([left_wrist.x - left_elbow.x, left_wrist.y - left_elbow.y])

    upper_arm_right = np.array([right_elbow.x - right_shoulder.x, right_elbow.y - right_shoulder.y])
    lower_arm_right = np.array([right_wrist.x - right_elbow.x, right_wrist.y - right_elbow.y])

    # 肩と肘、肘と手首の角度を計算
    left_arm_angle = calculate_arm_angle(upper_arm_left, lower_arm_left)
    right_arm_angle = calculate_arm_angle(upper_arm_right, lower_arm_right)
    
    score = calculate_arm_position_score_values(left_arm_angle, right_arm_angle)
    
    return score, left_arm_angle, right_arm_angle

# 肩と肘、肘と手首の角度を計算
def calculate_arm_angle(upper_arm, lower_arm):
    cosine_angle = np.dot(upper_arm, lower_arm) / (np.linalg.norm(upper_arm) * np.linalg.norm(lower_arm))
    angle = np.degrees(np.arccos(cosine_angle))
    return angle

# 腕が直線かのスコア
def calculate_arm_position_score_values(left_arm_angle, right_arm_angle):
    if left_arm_angle <= 20 and right_arm_angle <= 20:
        score = 3  # 満点
    elif left_arm_angle <= 45 and right_arm_angle <= 45:
        score = 2  # 中間
    elif left_arm_angle <= 70 and right_arm_angle <= 70:
        score = 1  # 低い
    else:
        score = 0  # 不適切
    return score