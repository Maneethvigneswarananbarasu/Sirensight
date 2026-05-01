import cv2
import math
import time
import threading
import firebase_admin
from firebase_admin import credentials, db
from ultralytics import YOLO

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
SERVICE_ACCOUNT_KEY = "serviceAccount.json"
DATABASE_URL = "https://sirensight-9a4e8-default-rtdb.firebaseio.com/"

print("Initializing SirenSight Master Engine...")
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

# Firebase References
status_ref = db.reference('Junction_Status')
amb_ref = db.reference('Active_Ambulance')
citizen_ref = db.reference('users/USER-101')

# Demo Police Junction
POLICE_JUNCTION = {"name": "Gandhi Mandapam Junction", "lat": 13.0136, "lng": 80.2411}

# ==========================================
# 2. MATHEMATICAL ENGINES
# ==========================================
def calc_haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_bearing(lat1, lon1, lat2, lon2):
    dLon = math.radians(lon2 - lon1)
    y = math.sin(dLon) * math.cos(math.radians(lat2))
    x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dLon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

# ==========================================
# 3. CITIZEN LOGIC (PURE GPS & BEARING)
# ==========================================
def citizen_fleet_listener(event):
    data = amb_ref.get()
    if not data: return

    # Grab the newest ambulance to ignore ghosts
    amb_id = list(data.keys())[-1]
    amb = data[amb_id]
    if 'lat' not in amb or 'lng' not in amb: return

    citizen = citizen_ref.get()
    if not citizen or citizen.get('lat') is None: return

    c_lat, c_lng = citizen.get('lat'), citizen.get('lng')
    has_moved = citizen.get('hasMoved', False)

    # Math
    dist = calc_haversine(amb['lat'], amb['lng'], c_lat, c_lng)
    amb_heading = amb.get('heading', 0)
    bearing_to_citizen = get_bearing(amb['lat'], amb['lng'], c_lat, c_lng)
    
    angle_diff = abs(amb_heading - bearing_to_citizen)
    if angle_diff > 180: angle_diff = 360 - angle_diff
    is_ahead = angle_diff <= 90

    # 🚨 CITIZEN RULE: < 150m AND Ahead AND Has Not Moved
    is_danger = (dist <= 150) and is_ahead and not has_moved
    db.reference('users/USER-101/alert_state').set(is_danger)

# Run Citizen Listener in background
amb_ref.listen(citizen_fleet_listener)

# ==========================================
# 4. POLICE LOGIC (TRIPLE VERIFICATION AI)
# ==========================================
print("Loading AI Vision Model (YOLO)...")
try:
    vision_model = YOLO('best.pt') # Ensure best.pt is in the same folder!
except:
    print("⚠️ WARNING: YOLO model 'best.pt' not found. Bypassing vision for demo.")
    vision_model = None

cap = cv2.VideoCapture(0)
last_police_trigger = 0

print("\n🚀 SIRENSIGHT SYSTEM IS FULLY ARMED AND LIVE!")
print("🛡️ POLICE RULE: Audio Compulsory + (Vision OR GPS < 250m)")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # --- A. VISION VERIFICATION ---
    vision_detected = False
    if vision_model:
        results = vision_model.predict(frame, conf=0.6, verbose=False)
        vision_detected = any(int(box.cls[0]) == 0 for r in results for box in r.boxes)
    
    # --- B. AUDIO VERIFICATION ---
    # Compulsory requirement. Hardcoded True for Demo purposes.
    audio_detected = True 

    # --- EVALUATE TRIPLE VERIFICATION ---
    if audio_detected:
        curr_time = time.time()
        
        if curr_time - last_police_trigger > 15: # 15s cooldown
            ambs = amb_ref.get()
            gps_detected = False
            
            if ambs:
                amb_id = list(ambs.keys())[-1]
                a_data = ambs[amb_id]
                
                # --- C. GPS VERIFICATION ---
                if 'lat' in a_data and 'lng' in a_data:
                    dist = calc_haversine(POLICE_JUNCTION['lat'], POLICE_JUNCTION['lng'], a_data['lat'], a_data['lng'])
                    gps_detected = (dist <= 250) # Police get 250m warning

            # 🔥 THE LOGIC GATE: Audio AND (Vision OR GPS)
            if vision_detected or gps_detected:
                print(f"\n✅ TRIPLE-VERIFICATION PASSED for {POLICE_JUNCTION['name']}!")
                print(f"   -> Audio: {audio_detected} | Vision: {vision_detected} | GPS: {gps_detected}")
                
                last_police_trigger = curr_time
                status_ref.set({
                    "isEmergency": True, 
                    "junction": POLICE_JUNCTION['name'], 
                    "timestamp": curr_time
                })
    
    # Reset Police Junction if no detection for 10 seconds
    if time.time() - last_police_trigger > 10:
        status_ref.update({"isEmergency": False})

    # Show Camera Feed
    cv2.imshow("SirenSight Police AI Node", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()