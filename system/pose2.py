import cv2
import mediapipe as mp

"""
class Pose2(self):
     def __init__():
"""
"""
#上半身どの動きまで終わったか
accept = 0


#返り値用の点数配列　リズム感良ければ8セットしてるはず.scoreは腕クロス、腕動き、膝の順
#満点[3, 4, 2]
score = [0, 0, 0]
"""

class Pose2:
     
    def __init__(self, mp_pose):
          self.mp_pose = mp_pose
          self.accept = 0
          self.accept_foot = 0
          self.times_pose_arm = 0
          self.times_pose_leg = 0
          self.score = [0,0,0]
    

    def score_calc(self, pose_landmarks):

                changeing = False
                add_score = [0,0,0]

                # pose_landmarksから右腕と左腕のポイントを取得する
                if pose_landmarks:
                    # ポイントのインデックスは以下の通り（詳細はMediapipeのドキュメントを参照）
                    right_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    right_elbow = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
                    right_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

                    left_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
                    left_elbow = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
                    left_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]

                    # 右小指と左小指のポイントの座標を取得
                    right_pinky = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_INDEX]
                    left_pinky = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_INDEX]

                    # 右ひざ、左ひざ、右足首、左足首の座標を取得
                    right_knee = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
                    left_knee = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
                    right_ankle = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
                    left_ankle = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]

                    """
                    # 取得したポイントの座標を表示
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_color = (255, 255, 255)
                    line_type = 2
                    """

                    # 右手のx座標が左手のx座標よりも左にある場合に"OK"と表示
                    if right_pinky.x > left_pinky.x and (self.accept == 0 or self.accept == 3):
                        ##cv2.putText(frame, '1point', (20, 70), font, font_scale, (0, 255, 0), line_type)
                        #始めの動作をしたとみなす(1)
                        self.accept = 1
                        changeing = True
                        add_score[0] += 1
                        print("add_score[0] += 1", add_score)
                        # 手が肘より上か右小指と左小指のy座標が右肘と左肘のy座標よりも小さい場合に"Excellent"と表示
                        if (right_pinky.y < right_elbow.y) and (left_pinky.y < left_elbow.y):
                            #cv2.putText(frame, '2point', (20, 90), font, font_scale, (0, 255, 0), line_type)
                            add_score[0] += 1
                            
                            # 各小指と各肘のy座標の差を計算
                            right_pinky_elbow_diff = abs(right_pinky.y - right_elbow.y)
                            left_pinky_elbow_diff = abs(left_pinky.y - left_elbow.y)
                            #手を肩付近まで持ってきているか
                            if (right_pinky_elbow_diff > abs(right_pinky.y - right_shoulder.y) and
                                left_pinky_elbow_diff > abs(left_pinky.y - left_shoulder.y)):
                                #cv2.putText(frame, '3point', (20, 110), font, font_scale, (255, 0, 0), line_type)
                                add_score[0] += 1

                    #腕を下に持ってきたか
                    if (right_shoulder.y < right_elbow.y < right_wrist.y and
                    left_shoulder.y < left_elbow.y < left_wrist.y) and self.accept == 1:
                        #cv2.putText(frame, 'below', (20, 150), font, font_scale, (0, 255, 255), line_type)
                        #腕を広げる動作中と見なす(2)
                        self.accept = 2
                        changeing = True

                        # 右hipと左hipの座標を取得
                        right_hip = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
                        left_hip = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
                        # 両手首のy座標が左右のhipのどちらかよりも大きい場合に"まっすぐ"と表示
                        if right_wrist.y > right_hip.y and left_wrist.y > left_hip.y:
                            #cv2.putText(frame, '1point', (20, 110), font, font_scale, (0, 255, 255), line_type)
                            add_score[1] += 1
                            print("add_score[1] += 1", add_score)
                    
                    if self.accept == 2:
                        # 各ポイントのx座標を取得
                        right_shoulder_x = right_shoulder.x
                        right_elbow_x = right_elbow.x
                        right_wrist_x = right_wrist.x

                        left_shoulder_x = left_shoulder.x
                        left_elbow_x = left_elbow.x
                        left_wrist_x = left_wrist.x
                        # 各ポイントのy座標を取得
                        right_shoulder_y = right_shoulder.y
                        right_elbow_y = right_elbow.y
                        right_wrist_y = right_wrist.y

                        left_shoulder_y = left_shoulder.y
                        left_elbow_y = left_elbow.y
                        left_wrist_y = left_wrist.y
                        # 肩、ひじ、手首のy座標の差を計算
                        diff_threshold = 0.3  # y座標の差の閾値

                        right_diff = abs(right_shoulder_y - right_elbow_y) + abs(right_elbow_y - right_wrist_y)
                        left_diff = abs(left_shoulder_y - left_elbow_y) + abs(left_elbow_y - left_wrist_y)

                        # ちゃんと全体的に上がってるか肩まで上がってる　肩、ひじ、手首のy座標がほぼ同じ場合に"5point"と表示
                        if (right_diff < diff_threshold and left_diff < diff_threshold):
                            #cv2.putText(frame, '2point', (20, 150), font, font_scale, (255, 0, 255), line_type)
                            #腕を広げたと見なす(2)
                            self.accept = 3
                            self.times_pose_arm +=1
                            changeing = True
                            add_score[1] += 1
                            print("add_score[1] += 1", add_score)

                            # まっすぐにするつもりがある 肩、ひじ、手首のx座標の比較を行い、"6point"と表示
                            if (left_wrist_x > left_elbow_x > left_shoulder_x > right_shoulder_x > right_elbow_x > right_wrist_x ):
                                #cv2.putText(frame, '3point', (20, 180), font, font_scale, (255, 0, 255), line_type)

                                # 肩からhipまでのx座標の差を計算
                                right_x_diff = abs(right_shoulder.x - right_hip.x)
                                left_x_diff = abs(left_shoulder.x - left_hip.x)

                                # 肩から手首までのy座標の差を計算
                                right_y_diff = abs(right_shoulder.y - right_wrist.y)
                                left_y_diff = abs(left_shoulder.y - left_wrist.y)
                                add_score[1] += 1

                                # 肩からhipまでのx座標の差より肩から手首までのy座標の差が大きい場合に"7point"と表示
                                if (right_diff < diff_threshold/3 and left_diff < diff_threshold/3):
                                    #cv2.putText(frame, '4point', (20, 200), font, font_scale, (255, 0, 255), line_type)
                                    add_score[1] += 1

                        
                        # 両足首のx座標の距離を計算
                    foot_distance = abs(right_ankle.x - left_ankle.x)

                    # 両ひざのx座標の距離を計算
                    knee_distance = abs(right_knee.x - left_knee.x)

                    # 両ひざが両足首のx座標の距離の二倍以上離れたら"footOK!"と表示
                    if knee_distance > 2 * foot_distance and self.accept_foot == 1:
                        #cv2.putText(frame, '0point', (20, 110), font, font_scale, (0, 255, 0), line_type)
                        #print("footok!")
                        #リズム感あるとする
                        if (self.accept == 1 or self.accept == 2) and changeing:
                            #cv2.putText(frame, '1point', (20, 110), font, font_scale, (0, 255, 0), line_type)
                            print("footok!2")
                            add_score[2] += 1
                        
                        add_score[2] = 1
                        self.accept_foot = 0
                        #何回屈伸したか
                        self.times_pose_leg += 1
                        print("add_score[2] += 1", add_score)
                        


                    else:
                        #cv2.putText(frame, 'footx', (20, 110), font, font_scale, (0, 255, 0), line_type)
                        #print("footx")
                        if (self.accept == 0 or self.accept ==3 ) and changeing and self.accept_foot == 0:
                            #cv2.putText(frame, '1point', (20, 110), font, font_scale, (0, 255, 0), line_type)
                            print("footok!3")
                            add_score[2] += 1
                        
                        self.accept_foot = 1

                    self.score[0] += add_score[0]/8
                    self.score[1] += add_score[1]/8
                    self.score[2] += add_score[2]/8

                    """
                    if self.times_pose_arm > 8:
                        self.score[0] -= self.times_pose_arm * 0.1
                        self.score[1] -= self.times_pose_arm * 0.1
                    elif self.times_pose_leg > 8:
                        self.score[2] -= self.times_pose_leg * 0.1
                    """
                return self.score
