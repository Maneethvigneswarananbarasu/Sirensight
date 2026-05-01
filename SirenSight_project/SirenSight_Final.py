import cv2
import numpy as np
import librosa
import pyaudio
import tensorflow as tf
from ultralytics import YOLO
import firebase_admin
from firebase_admin import credentials, db, messaging
import threading
import time
import math

# --- CONFIG ---
CITIZEN_TOPIC = "lane_a"
POLICE_TOPIC = "police"
MAX_RADIUS_KM = 2.0 

# --- FIREBASE ---
cred = credentials.Certificate("serviceAccount.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sirensight-9a4e8-default-rtdb.firebaseio.com/'
    })

status_ref = db.reference('Junction_Status')
ambulance_ref = db.reference('Active_Ambulance')
junction_ref = db.reference('Junctions')

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def trigger_alert(lat, lng, j_id):
    """Updates DB to TRUE and sends the wake-up notification."""
    try:
        status_ref.set({"isEmergency": True, "junction": j_id, "timestamp": time.time()})
        
        payload = {"title": "🚨 AMBULANCE NEARBY", "body": "Move Left! Continuous Alert Active.", "lat": str(lat), "lng": str(lng)}
        messaging.send(messaging.Message(data=payload, topic=CITIZEN_TOPIC))
        print(f"🔥 Alert Triggered for {j_id}")
    except Exception as e:
        print("Error:", e)

# --- MODELS ---
vision_model = YOLO('best.pt')
audio_model = tf.keras.models.load_model('siren_ear.h5')

cap = cv2.VideoCapture(0)
last_trigger_time = 0

print("🚀 SirenSight Final System Running...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # AI Detection
    results = vision_model.predict(frame, conf=0.6, verbose=False)
    vision_detected = any(int(box.cls[0]) == 0 for r in results for box in r.boxes)
    
    # Simple Audio Check (Mocking logic for brevity, use your librosa code here)
    audio_detected = True # Replace with your is_siren() function

    if vision_detected and audio_detected:
        curr_time = time.time()
        if curr_time - last_trigger_time > 15: # 15s cooldown between notifications
            
            ambs = ambulance_ref.get()
            juncs = junction_ref.get()

            if ambs and juncs:
                for a_id, a_data in ambs.items():
                    for j_id, j_data in juncs.items():
                        dist = get_distance(j_data['lat'], j_data['lng'], a_data['lat'], a_data['lng'])
                        if dist <= MAX_RADIUS_KM:
                            last_trigger_time = curr_time
                            threading.Thread(target=trigger_alert, args=(a_data['lat'], a_data['lng'], j_id)).start()
    
    # Reset logic: If no detection for 10 seconds, clear the emergency
    if time.time() - last_trigger_time > 10:
        status_ref.update({"isEmergency": False})

    cv2.imshow("Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()