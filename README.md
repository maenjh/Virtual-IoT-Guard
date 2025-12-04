# Virtual-IoT-Guard (Smart Edition)

Virtual-IoT-Guard has been upgraded to a modern **Smart Security & Environment System**. It now features AI-powered face detection, virtual environmental sensors, and a real-time web dashboard for monitoring and control.

## 🌟 New Features
- **🧠 AI Face Detection**: Uses OpenCV Haar Cascades to detect intruders (faces).
- **🌡️ Virtual Environment Sensor**: Simulates Temperature & Humidity data via **Virtual Serial Port**.
- **💻 Web Dashboard**: A modern interface to monitor security status and environment data.
- **⚡ Real-time Alerts**: WebSocket-based communication for instant updates.
- **🎮 Remote Control**: Control a virtual "Fan" from the dashboard.

## 🏗️ System Architecture

```
[Webcam] → [Smart Camera] ──┐
                            │
[Virtual Sensor] ──(Serial)─┴→ [MQTT Broker] ←→ [FastAPI Server] ←→ [Web Dashboard]
(Temp/Humid)     (Simulation)   (Mosquitto)      (WebSocket)        (Monitor/Control)
```

## 📁 Project Structure

```
Virtual-IoT-Guard/
├── app/                        # Web Application (Backend & Frontend)
│   ├── main.py                 # FastAPI Server & MQTT Client
│   ├── templates/              # HTML Templates
│   └── static/                 # CSS & JS
├── sensors/                    # IoT Sensors
│   ├── smart_camera.py         # AI Camera Module
│   └── virtual_environment_sensor.py # Virtual Serial Sensor (Temp/Humid)
├── requirements.txt            # Dependencies
└── README.md
```

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Dashboard (Control Center)
Open a terminal and run the FastAPI server:
```bash
uvicorn app.main:app --reload
```
> Open your browser and go to `http://127.0.0.1:8000`

### 3. Start the Smart Camera (Security)
Open a **new terminal** and run the camera module:
```bash
python sensors/smart_camera.py
```

### 4. Start the Virtual Sensor (Environment)
Open another **new terminal** and run the virtual sensor:
```bash
python sensors/virtual_environment_sensor.py
```

## 📚 Educational Concepts
This project demonstrates key IoT concepts without physical hardware:
1.  **Sensor Simulation**: Generating synthetic sensor data.
2.  **Serial Communication**: Simulating UART communication used by Arduino/ESP32.
3.  **MQTT Protocol**: Pub/Sub messaging pattern.
4.  **Full-Stack IoT**: Connecting hardware (simulated) to a web frontend.

