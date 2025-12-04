import time
import json
import random
import paho.mqtt.client as mqtt
import threading
import queue

# ==========================================
# 1. Virtual Serial Port Simulation (시리얼 통신 모사)
# ==========================================
class VirtualSerial:
    """
    실제 하드웨어 시리얼 포트(Arduino 등)를 흉내내는 클래스입니다.
    실제 센서가 없어도 시리얼 통신 코드를 학습할 수 있습니다.
    """
    def __init__(self):
        self.buffer = queue.Queue()
        self.is_open = True
        print("🔌 [Virtual Serial] Port '/dev/ttyUSB0' opened (Simulated)")
        
        # 백그라운드에서 가상 센서 데이터를 생성하는 스레드 시작
        self._sensor_thread = threading.Thread(target=self._generate_sensor_data)
        self._sensor_thread.daemon = True
        self._sensor_thread.start()

    def _generate_sensor_data(self):
        """가상의 온도/습도 데이터를 생성하여 버퍼에 넣습니다."""
        while self.is_open:
            # 가상 센서 값 생성 (랜덤 변화)
            temp = round(random.uniform(20.0, 30.0), 1)
            humidity = round(random.uniform(40.0, 60.0), 1)
            
            # 아두이노가 보내는 데이터 형식 시뮬레이션 (JSON 문자열 + 줄바꿈)
            data = json.dumps({"temp": temp, "humidity": humidity}) + "\n"
            
            # 시리얼 버퍼에 데이터 쓰기
            self.buffer.put(data.encode('utf-8'))
            time.sleep(2) # 2초마다 데이터 생성

    def readline(self):
        """시리얼 버퍼에서 한 줄을 읽어옵니다."""
        if not self.buffer.empty():
            return self.buffer.get()
        return b""

    def in_waiting(self):
        """버퍼에 대기 중인 데이터가 있는지 확인합니다."""
        return not self.buffer.empty()

    def write(self, data):
        """장치로 데이터를 보냅니다 (Actuator 제어 시뮬레이션)"""
        command = data.decode('utf-8').strip()
        print(f"📤 [Serial TX] Command sent to device: {command}")
        if command == "FAN_ON":
            print("   --> 💨 Virtual Fan Started!")
        elif command == "FAN_OFF":
            print("   --> 🛑 Virtual Fan Stopped!")

# ==========================================
# 2. IoT Gateway Logic (MQTT Publisher)
# ==========================================

# MQTT 설정
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC_DATA = "home/livingroom/environment"
MQTT_TOPIC_CONTROL = "home/livingroom/fan/control"
MQTT_TOPIC_TRIGGER = "home/sensor/trigger"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT Broker (Result: {rc})")
    # 팬 제어 명령 및 센서 트리거 구독
    client.subscribe(MQTT_TOPIC_CONTROL)
    client.subscribe(MQTT_TOPIC_TRIGGER)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    if topic == MQTT_TOPIC_CONTROL:
        # MQTT로 받은 제어 명령을 시리얼 포트로 전달 (Gateway 역할)
        print(f"📩 [MQTT RX] Received control command: {payload}")
        ser.write(payload.encode())
        
    elif topic == MQTT_TOPIC_TRIGGER:
        print(f"📩 [MQTT RX] Trigger Received! Requesting Sensor Data...")
        # 트리거를 받으면 시리얼 버퍼에서 최신 데이터를 읽어서 전송
        # 버퍼에 쌓인 데이터를 모두 읽어 가장 최신 값만 사용 (Flush)
        last_data = None
        while ser.in_waiting():
            last_data = ser.readline()
            
        if last_data:
            try:
                decoded_data = last_data.decode('utf-8').strip()
                if decoded_data:
                    print(f"📤 [MQTT TX] Sending Sensor Data: {decoded_data}")
                    client.publish(MQTT_TOPIC_DATA, decoded_data)
            except Exception as e:
                print(f"Error parsing data: {e}")
        else:
            print("⚠️ No data in serial buffer yet.")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

# 가상 시리얼 포트 연결
ser = VirtualSerial()

print("🚀 IoT Sensor Gateway Started")
print("Waiting for commands or triggers...")

try:
    while True:
        # 메인 루프는 이제 트리거 대기 상태이므로 별도 작업 없음
        # 연결 유지를 위해 sleep
        time.sleep(1)

except KeyboardInterrupt:
    print("Terminating...")
    client.loop_stop()
