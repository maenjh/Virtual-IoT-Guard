# Virtual-IoT-Guard

Virtual-IoT-Guard is a hardware-free IoT project that turns your webcam into a motion-activated security camera. It uses OpenCV for visual detection and the MQTT protocol to send alerts to a virtual smart device, perfectly simulating a real-world sensor-to-actuator workflow.

## 📋 Project Overview

This project consists of a **motion detection security system** using a webcam and a **virtual IoT lighting device**. It simulates IoT sensor-to-actuator communication flow without requiring any physical hardware.

### Key Features
- �� **Real-time Motion Detection**: Automatically detects movement through webcam
- 📡 **MQTT Protocol Communication**: IoT messaging through public broker
- 💡 **Virtual Smart Lighting**: Automatic light control upon motion detection
- ⏱️ **Cooldown System**: Message transmission every 5 seconds to prevent unnecessary alerts

## 🏗️ System Architecture

```
[웹캠] → [Camera_Publisher.py] → [MQTT Broker] → [Virtual_Light.py] → [조명 제어]
         (모션 감지)              (test.mosquitto.org)    (메시지 구독)
```

## 📁 프로젝트 구조

```
iotcamASKII/
├── Camera_Publisher.py    # 웹캠 모션 감지 및 MQTT 메시지 발행
└── Virtual_Light.py       # MQTT 메시지 구독 및 가상 조명 제어
```

## 🔧 구성 요소

### 1. Camera_Publisher.py (카메라 센서 모듈)
웹캠을 통해 실시간으로 영상을 분석하고 움직임을 감지하는 Publisher 역할을 수행합니다.

**주요 기능:**
- OpenCV를 사용한 실시간 비디오 캡처
- 프레임 간 차이 분석을 통한 모션 감지
- 가우시안 블러를 활용한 노이즈 제거
- 움직임 감지 시 MQTT 메시지 발행 (`MOTION_DETECTED`)
- 5초 쿨다운으로 메시지 발행 빈도 제어
- 640x480 해상도로 화면 표시

**동작 원리:**
1. 웹캠에서 프레임을 읽어옴
2. 흑백 변환 및 블러 처리로 노이즈 감소
3. 이전 프레임과의 차이를 계산
4. 일정 크기 이상의 변화가 감지되면 모션으로 판단
5. MQTT 토픽 `home/entrance/motion`으로 알림 전송

### 2. Virtual_Light.py (가상 조명 액추에이터)
MQTT 브로커로부터 메시지를 구독하고 조명 제어를 시뮬레이션하는 Subscriber 역할을 수행합니다.

**주요 기능:**
- MQTT 토픽 구독 (`home/entrance/motion`)
- `MOTION_DETECTED` 메시지 수신 시 가상 조명 켜기
- 실시간 메시지 수신 및 처리

**동작 원리:**
1. MQTT 브로커에 연결
2. 특정 토픽을 구독
3. 메시지 수신 시 `on_message` 콜백 함수 실행
4. 조명 제어 시뮬레이션 (콘솔 출력)

## 🚀 시작하기

### 필수 요구사항
```bash
pip install opencv-python
pip install paho-mqtt
```

### 실행 방법

1. **가상 조명 디바이스 실행** (터미널 1)
```bash
python Virtual_Light.py
```

2. **카메라 모션 센서 실행** (터미널 2)
```bash
python Camera_Publisher.py
```

3. 웹캠 앞에서 움직이면 모션이 감지되고, Virtual_Light에서 조명이 켜지는 메시지를 확인할 수 있습니다.

4. 종료하려면 `q` 키를 누르거나 `Ctrl+C`를 입력하세요.

## ⚙️ 설정

### MQTT 브로커 변경
기본적으로 `test.mosquitto.org` 공개 브로커를 사용합니다. 다른 브로커를 사용하려면:

```python
MQTT_BROKER = "your-broker-address"  # 브로커 주소 변경
MQTT_TOPIC = "your/custom/topic"     # 토픽 변경
```

### 모션 감지 민감도 조절
`Camera_Publisher.py`에서 다음 파라미터를 조정할 수 있습니다:

```python
COOLDOWN_SECONDS = 5        # 메시지 발행 간격 (초)
cv2.contourArea(c) < 500    # 최소 감지 면적 (작을수록 민감)
cv2.threshold(frame_delta, 25, 255, ...)  # 임계값 (작을수록 민감)
```

## 🛠️ 기술 스택

- **Python 3.x**
- **OpenCV (cv2)**: 컴퓨터 비전 및 이미지 처리
- **paho-mqtt**: MQTT 프로토콜 클라이언트
- **MQTT Protocol**: IoT 디바이스 간 경량 통신
- **test.mosquitto.org**: 무료 공개 MQTT 브로커

## 📊 동작 흐름도

```
1. Camera_Publisher 시작
   ↓
2. 웹캠에서 프레임 캡처
   ↓
3. 모션 감지 알고리즘 실행
   ↓
4. 움직임 감지됨? 
   ├─ Yes → MQTT 메시지 발행 (5초 쿨다운)
   └─ No → 다음 프레임 분석
   ↓
5. Virtual_Light가 메시지 수신
   ↓
6. 💡 조명 켜기 시뮬레이션
```

## 🎯 활용 사례

- 스마트 홈 보안 시스템 프로토타입
- IoT 통신 프로토콜 학습
- 컴퓨터 비전 기반 모션 감지 실습
- MQTT 기반 센서-액추에이터 통신 데모
- 실제 하드웨어 없이 IoT 시스템 테스트

## 🔍 트러블슈팅

### 카메라를 열 수 없습니다
- 웹캠이 제대로 연결되어 있는지 확인
- 다른 프로그램에서 카메라를 사용 중인지 확인
- `cv2.VideoCapture(0)`의 `0`을 `1`이나 다른 숫자로 변경

### MQTT 연결 실패
- 인터넷 연결 확인
- 방화벽 설정 확인 (포트 1883)
- 다른 공개 브로커 시도 (예: `broker.hivemq.com`)

### 모션 감지가 너무 민감하거나 둔감함
- `cv2.contourArea(c) < 500` 값을 조정
- 조명 환경을 개선하거나 웹캠 위치 변경

## 📝 라이선스

이 프로젝트는 교육 및 학습 목적으로 자유롭게 사용할 수 있습니다.

## 👥 기여

개선 사항이나 버그 리포트는 언제든지 환영합니다!

