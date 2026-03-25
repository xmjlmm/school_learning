import cv2
import mediapipe as mp
import socket
import numpy as np

# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8,
#                        min_tracking_confidence=0.1)

# # 设置TCP套接字
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 65431)
# sock.bind(server_address)
# sock.listen(1)

cap = cv2.VideoCapture(0)

# 初始化累计变量和前一帧位置变量
cumulative_x, cumulative_y, cumulative_z = 0, 0, 0
previous_x, previous_y, previous_z = None, None, None
not_found = 0


# 定义函数：判断手指是否直立
def is_finger_straight(landmarks, finger_tip_idx, finger_dip_idx, palm_idx):
    """ 判断某个手指是否是直立的 """
    if finger_tip_idx == 4:
        v1 = landmarks[finger_tip_idx] - landmarks[palm_idx]  # MCP到DIP的向量
        v2 = landmarks[finger_dip_idx] - landmarks[palm_idx]  # DIP到TIP的向量
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return cos_angle > 0.97  # 余弦值在0.97以上可以认为是近似直立
    tip_to_palm_dist = np.linalg.norm(landmarks[finger_tip_idx] - landmarks[palm_idx])
    dip_to_palm_dist = np.linalg.norm(landmarks[finger_dip_idx] - landmarks[palm_idx])
    return tip_to_palm_dist > dip_to_palm_dist


def mode(hand_landmarks):
    x_min, y_min, x_max, y_max = get_bounding_box(hand_landmarks)
    finger_tips = [12, 16, 20]
    for tip in finger_tips:
        fingertip = hand_landmarks.landmark[tip]
        if fingertip.x == x_max or fingertip.x == x_min or fingertip.y == y_max or fingertip.y == y_min:
            return 1  # 张开
    return 0  # 拳头


def triangle_area(point1, point2, point3):
    # 计算边长
    a = np.linalg.norm(point2 - point1)
    b = np.linalg.norm(point3 - point2)
    c = np.linalg.norm(point1 - point3)

    # 使用海伦公式计算面积
    s = (a + b + c) / 2  # 半周长
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))  # 面积

    return area


def get_bounding_box(hand_landmarks):
    x_min, y_min = 1.0, 1.0
    x_max, y_max = 0.0, 0.0
    for landmark in hand_landmarks.landmark:
        x, y = landmark.x, landmark.y
        # 分别更新 x_min, y_min, x_max, y_max
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x)
        y_max = max(y_max, y)
    return (x_min, y_min, x_max, y_max)


# print('等待来自 Unity 的连接...')
# connection, client_address = sock.accept()
# print('Unity 连接成功！')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_handedness:
        for hand_landmarks in results.multi_hand_landmarks:
            # 提取21个手部关键点
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])

            # 判断手指状态，0代表未直立，1代表直立
            fingers_state = [
                int(is_finger_straight(landmarks, 4, 2, 0)),  # 拇指
                int(is_finger_straight(landmarks, 8, 5, 0)),  # 食指
                int(is_finger_straight(landmarks, 12, 9, 0)),  # 中指
                int(is_finger_straight(landmarks, 16, 13, 0)),  # 无名指
                int(is_finger_straight(landmarks, 20, 17, 0))  # 小指
            ]

            point0 = landmarks[0]  # 关键点0
            point5 = landmarks[5]  # 关键点5
            point17 = landmarks[17]  # 关键点17

            gesture = mode(hand_landmarks)

            # 计算手掌的相对面积（fig_size）
            x_min, y_min, x_max, y_max = get_bounding_box(hand_landmarks)
            fig_size = (x_max - x_min) * (y_max - y_min)
            # depth_info = fig_size  # 将 fig_size 转换为合适的深度数据
            depth_info = triangle_area(point0, point5, point17)
            # 获取当前帧的手掌位置 (landmark[9])，并缩放为360*360的坐标系
            current_x = hand_landmarks.landmark[5].x * 120
            current_y = hand_landmarks.landmark[5].y * 70

            current_z = depth_info * 1
            # current_z = hand_landmarks.landmark[5].z *100
            # 如果有上一帧数据，计算差值并进行累加
            if previous_x is not None and previous_y is not None:
                delta_x = current_x - previous_x
                delta_y = current_y - previous_y
                delta_z = current_z - previous_z

                # 累加差值
                cumulative_x += delta_x
                cumulative_y += delta_y
                cumulative_z += delta_z
            else:
                # 如果是第一帧，直接初始化前一帧为当前帧
                cumulative_x = 0
                cumulative_y = 0
                cumulative_z = 0

            # 更新前一帧的位置
            previous_x = current_x
            previous_y = current_y
            previous_z = current_z

            # 构建发送给 Unity 的消息: "手势,累计x,累计y,深度信息"
            # message = f"{gesture},{cumulative_x},{cumulative_y},{cumulative_z}\n"
            message = f"{fingers_state[0]},{fingers_state[1]},{fingers_state[2]},{fingers_state[3]},{fingers_state[4]},{cumulative_x},{cumulative_y},{cumulative_z}\n"
            print(fingers_state)
            try:
                connection.sendall(message.encode('utf-8'))
            except:
                print('Unity 断开连接！')
                connection, client_address = sock.accept()
                print('Unity 重接成功！')
        # print(f"cumulative_x: {cumulative_x}, cumulative_y: {cumulative_y}, cumulative_z: {cumulative_z}")
        not_found = 0
    else:
        not_found = not_found + 1
    if not_found > 5:
        previous_x, previous_y = None, None
        cumulative_x = 0
        cumulative_y = 0
        not_found = 0
        print("手掌未找到，累计位置重置为0")
    # OpenCV 处理
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
# connection.close()
# sock.close()
