import cv2
import paho.mqtt.client as mqtt
import time
import json
import sys
import os
import mediapipe as mp

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC_EVENT = "home/security/camera/event"
MQTT_TOPIC_TRIGGER = "home/sensor/trigger"

# Initialize MQTT Client
client = mqtt.Client()

def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, 1883, 60)
        print(f"✅ Connected to MQTT Broker: {MQTT_BROKER}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

# Face Detection Setup (Haar Cascade)
# Handle cases where cv2.data is not available (older OpenCV versions)
if hasattr(cv2, 'data'):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
else:
    # Fallback: try to construct path relative to cv2 module
    cascade_path = os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml')
    
    # If still not found, try local file or default system path
    if not os.path.exists(cascade_path):
        cascade_path = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print(f"⚠️ Warning: Could not load Haar Cascade from {cascade_path}")
    print("Attempting to download haarcascade_frontalface_default.xml...")
    
    try:
        import urllib.request
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(url, "haarcascade_frontalface_default.xml")
        print("✅ Download successful.")
        cascade_path = "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
    except Exception as e:
        print(f"❌ Download failed: {e}")

if face_cascade.empty():
    print("❌ Error: Failed to load Haar Cascade Classifier. Exiting.")
    sys.exit(1)

# Hand Detection Setup (MediaPipe)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def start_surveillance():
    cap = cv2.VideoCapture(0)
    
    # Set resolution to 640x480 to reduce window size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("🎥 Smart Surveillance System Active")
    print("Press 'q' to quit.")

    last_detection_time = 0
    last_hand_time = 0
    COOLDOWN = 3.0  # Seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Convert to RGB for hand detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        current_time = time.time()

        # 1. Face Detection
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        detected_face = len(faces) > 0

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "INTRUDER", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        if detected_face and (current_time - last_detection_time > COOLDOWN):
            payload = {
                "event": "intrusion_detected",
                "timestamp": current_time,
                "count": len(faces),
                "message": "⚠️ Intruder detected at main entrance!"
            }
            client.publish(MQTT_TOPIC_EVENT, json.dumps(payload))
            print(f"📡 Alert Sent: {payload['message']}")
            last_detection_time = current_time

        # 2. Hand Detection
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Send Trigger if cooldown passed
            if current_time - last_hand_time > COOLDOWN:
                client.publish(MQTT_TOPIC_TRIGGER, "GET_ENV_DATA")
                print("✋ Hand Detected! Requesting Environment Data...")
                last_hand_time = current_time
                
                # Visual feedback
                cv2.putText(frame, "DATA REQUESTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Smart Security Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    connect_mqtt()
    start_surveillance()
