import cv2
import mediapipe as mp
import numpy as np
import time

# 点数付けに関するファイル
import shoulders_slanting
import arm_straight
import arm_up

# 
import database

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# VideoCaptureを使ってカメラ入力を取得
cap = cv2.VideoCapture(0)

# スコアを格納するリストを初期化
shoulder_scores = []
arm_scores = []
arm_up_scores = []

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    
    start_time = time.time()  # 開始時刻を記録
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # 画像の幅を取得
        image_height, image_width, _ = image.shape
        
        # カメラのフレームを処理
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        # 姿勢ランドマークを描画
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # 点数づけを行う関数を実行
            current_time = time.time()
            # 開始から15秒まで実行
            if current_time - start_time < 15:
                # 肩が地面に対して平行か判定
                shoulder_score, shoulder_angle = shoulders_slanting.calculate_shoulder_score(results.pose_landmarks)
                shoulder_scores.append(shoulder_score)

                # 腕が曲がってないか判定
                arm_score, left_arm_angle, right_arm_angle = arm_straight.calculate_arm_position_score(results.pose_landmarks)
                arm_scores.append(arm_score)

            if (0 <= current_time - start_time < 10) or (12 <= current_time - start_time < 14):
                # 腕が体から離れていないか判定
                arm_up_score, left_arm_up_distance, right_arm_up_distance = arm_up.calculate_arm_up_score(results.pose_landmarks, image_width)
                arm_up_scores.append(arm_up_score)

            # 画面上にスコアを表示
            if current_time - start_time < 15:
                cv2.putText(image, f'Shoulder Score: {shoulder_score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f'Shoulder Angle: {shoulder_angle:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f'Arm Score: {arm_score}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f'Left Arm Angle: {left_arm_angle:.2f}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f'Right Arm Angle: {right_arm_angle:.2f}', (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            if (0 <= current_time - start_time < 10) or (12 <= current_time - start_time < 14):
                cv2.putText(image, f'Arm Up Score: {arm_up_score}', (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f'Left Arm Up Distance: {left_arm_up_distance:.2f}', (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f'Right Arm Up Distance: {right_arm_up_distance:.2f}', (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # 結果を表示
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

# スコアの平均値を計算
def score_mean(scores):
    average = np.mean(scores)
    print(f'スコア：{average}')
    return average

shoulder_avg = score_mean(shoulder_scores)
arm_avg = score_mean(arm_scores)
arm_up_avg = score_mean(arm_up_scores)

conn = database.get_database()

# カーソルオブジェクトを作成
cursor = conn.cursor()

# データベースにスコアを追加
sql = "INSERT INTO scores (shoulder_score, arm_score, arm_up_score) VALUES (%s, %s, %s)"
cursor.execute(sql, (shoulder_avg, arm_avg, arm_up_avg))

cap.release()
cv2.destroyAllWindows()

# 必要に応じてトランザクションをコミット
conn.commit()

# カーソルと接続を閉じる
cursor.close()
conn.close()