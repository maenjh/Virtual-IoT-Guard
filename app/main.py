from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import paho.mqtt.client as mqtt
import threading
import json
import asyncio

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Store connected websockets
active_connections = []

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC_CAMERA = "home/security/camera/event"
MQTT_TOPIC_ENV = "home/livingroom/environment"
MQTT_TOPIC_FAN_CONTROL = "home/livingroom/fan/control"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC_CAMERA)
    client.subscribe(MQTT_TOPIC_ENV)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        topic = msg.topic
        
        # Broadcast to all connected websockets
        message_data = {
            "topic": topic,
            "payload": json.loads(payload) if payload.startswith('{') else payload
        }
        
        # We need to run this in the event loop
        asyncio.run_coroutine_threadsafe(broadcast_message(json.dumps(message_data)), loop)
    except Exception as e:
        print(f"Error processing message: {e}")

async def broadcast_message(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            active_connections.remove(connection)

# Start MQTT Client in a separate thread
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/fan/{action}")
async def control_fan(action: str):
    if action not in ["on", "off"]:
        return {"error": "Invalid action"}
    
    command = "FAN_ON" if action == "on" else "FAN_OFF"
    client.publish(MQTT_TOPIC_FAN_CONTROL, command)
    return {"status": "success", "command": command}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection open
    except:
        active_connections.remove(websocket)
