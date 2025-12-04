# Virtual-IoT-Guard (Smart Edition)

Virtual-IoT-Guard has been upgraded to a modern **Smart Security & Environment System**. It now features AI-powered face detection, **Hand Gesture Control**, virtual environmental sensors, and a real-time web dashboard.

Virtual-IoT-Guard가 최신 **스마트 보안 및 환경 시스템**으로 업그레이드되었습니다. 이제 AI 기반 얼굴 인식, **손 제스처 제어**, 가상 환경 센서, 그리고 실시간 웹 대시보드를 제공합니다.

## 🌟 New Features (주요 기능)
- **🧠 AI Face Detection (AI 얼굴 인식)**: Uses OpenCV Haar Cascades to detect intruders (faces).
  - OpenCV Haar Cascades를 사용하여 침입자(얼굴)를 감지합니다.
- **✋ Hand Gesture Trigger (손 제스처 트리거)**: Uses **MediaPipe** to detect hands. When a hand is detected, it requests fresh environment data.
  - **MediaPipe**를 사용하여 손을 감지합니다. 손이 감지되면 최신 환경 데이터를 요청합니다.
- **🌡️ Virtual Environment Sensor (가상 환경 센서)**: Simulates Temperature & Humidity data via **Virtual Serial Port**. It responds to triggers from the camera.
  - **가상 시리얼 포트**를 통해 온도 및 습도 데이터를 시뮬레이션합니다. 카메라의 트리거 신호에 반응합니다.
- **💻 Web Dashboard (웹 대시보드)**: A modern interface to monitor security status and environment data.
  - 보안 상태와 환경 데이터를 모니터링할 수 있는 현대적인 인터페이스를 제공합니다.
- **⚡ Real-time Alerts (실시간 알림)**: WebSocket-based communication for instant updates.
  - WebSocket 기반 통신으로 즉각적인 업데이트를 제공합니다.
- **🎮 Remote Control (원격 제어)**: Control a virtual "Fan" from the dashboard.
  - 대시보드에서 가상의 "팬(Fan)"을 제어할 수 있습니다.

## 🏗️ System Architecture (시스템 아키텍처)

```
[Webcam] → [Smart Camera] ──(Trigger)──┐
           (Face/Hand AI)              │
                                       ▼
[Virtual Sensor] ──(Serial)──→ [MQTT Broker] ←→ [FastAPI Server] ←→ [Web Dashboard]
(Temp/Humid)     (Simulation)   (Mosquitto)      (WebSocket)        (Monitor/Control)
```

## 📁 Project Structure (프로젝트 구조)

```
Virtual-IoT-Guard/
├── app/                        # Web Application (Backend & Frontend) / 웹 애플리케이션
│   ├── main.py                 # FastAPI Server & MQTT Client / 서버 및 MQTT 클라이언트
│   ├── templates/              # HTML Templates / HTML 템플릿
│   └── static/                 # CSS & JS / 정적 파일
├── sensors/                    # IoT Sensors / IoT 센서
│   ├── smart_camera.py         # AI Camera Module / AI 카메라 모듈
│   └── virtual_environment_sensor.py # Virtual Serial Sensor (Temp/Humid) / 가상 시리얼 센서
├── requirements.txt            # Dependencies / 의존성 패키지 목록
└── README.md
```

## 🚀 How to Run (실행 방법)

### 1. Install Dependencies (의존성 설치)
```bash
pip install -r requirements.txt
```

### 2. Start the Web Dashboard (웹 대시보드 실행)
Open a terminal and run the FastAPI server:
터미널을 열고 FastAPI 서버를 실행합니다:
```bash
uvicorn app.main:app --reload
```
> Open your browser and go to `http://127.0.0.1:8000`
> 브라우저를 열고 `http://127.0.0.1:8000`으로 접속하세요.

### 3. Start the Smart Camera (스마트 카메라 실행)
Open a **new terminal** and run the camera module:
**새 터미널**을 열고 카메라 모듈을 실행합니다:
```bash
python sensors/smart_camera.py
```

### 4. Start the Virtual Sensor (가상 센서 실행)
Open another **new terminal** and run the virtual sensor:
또 다른 **새 터미널**을 열고 가상 센서를 실행합니다:
```bash
python sensors/virtual_environment_sensor.py
```

## 📚 Educational Concepts (학습 요소)
This project demonstrates key IoT concepts without physical hardware:
이 프로젝트는 물리적인 하드웨어 없이 핵심 IoT 개념을 보여줍니다:

1.  **Sensor Simulation (센서 시뮬레이션)**: Generating synthetic sensor data.
    - 가상의 센서 데이터를 생성합니다.
2.  **Serial Communication (시리얼 통신)**: Simulating UART communication used by Arduino/ESP32.
    - Arduino/ESP32에서 사용하는 UART 통신을 시뮬레이션합니다.
3.  **MQTT Protocol (MQTT 프로토콜)**: Pub/Sub messaging pattern.
    - Pub/Sub 메시징 패턴을 학습합니다.
4.  **Full-Stack IoT (풀스택 IoT)**: Connecting hardware (simulated) to a web frontend.
    - 하드웨어(시뮬레이션)와 웹 프론트엔드를 연결합니다.

