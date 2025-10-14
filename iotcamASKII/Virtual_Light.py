import paho.mqtt.client as mqtt

# MQTT 설정
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "home/entrance/motion" # 메시지를 받을 주소 (토픽)

# 메시지를 받았을 때 실행될 함수
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(f"메시지 수신! 토픽: {msg.topic}, 메시지: {message}")
    if message == "MOTION_DETECTED":
        print("💡 현관 조명을 켭니다!")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_message = on_message # 메시지 수신 시 on_message 함수 호출

# 브로커에 연결
print(f"'{MQTT_TOPIC}' 토픽을 구독합니다...")
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

# 메시지를 계속 듣기 위해 무한 루프 실행
client.loop_forever()