import cv2
import paho.mqtt.client as mqtt
import time

# MQTT 설정
MQTT_BROKER = "test.mosquitto.org"  # 무료 공개 브로커
MQTT_TOPIC = "home/entrance/motion" # 메시지를 보낼 주소 (토픽)

# MQTT 클라이언트 설정
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# 웹캠 설정
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("오류: 카메라를 열 수 없습니다.")
    exit()

# 이전 프레임 저장을 위한 변수
prev_frame = None
# 메시지 발행 쿨다운을 위한 변수
last_published_time = 0
COOLDOWN_SECONDS = 5 # 5초에 한 번만 메시지 보내기

print("움직임 감지를 시작합니다... (종료하려면 'q'를 누르세요)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 흑백으로 변환하고 블러 처리하여 노이즈 감소
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    # 현재 프레임과 이전 프레임의 차이 계산
    frame_delta = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # 변화가 감지된 영역 찾기
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) < 500: # 너무 작은 변화는 무시
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 움직임이 감지되고 쿨다운 시간이 지났으면 MQTT 메시지 발행
    current_time = time.time()
    if motion_detected and (current_time - last_published_time > COOLDOWN_SECONDS):
        message = "MOTION_DETECTED"
        print(f"[{time.ctime()}] 움직임 감지! MQTT 메시지 발행: {message}")
        client.publish(MQTT_TOPIC, message)
        last_published_time = current_time

    # --- ✨ 수정된 부분 시작 ✨ ---
    # 원하는 크기로 프레임 사이즈 조절 (예: 가로 640, 세로 480)
    resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

    # 화면에 '조절된' 영상 표시
    cv2.imshow("Security Cam", resized_frame)
    # --- ✨ 수정된 부분 끝 ✨ ---
    
    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = gray

# 종료 처리
cap.release()
cv2.destroyAllWindows()
client.disconnect()